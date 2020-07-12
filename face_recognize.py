import face_recognition
import docopt
import sklearn
from sklearn import svm
import os
import utils
import datetime
from datetime import datetime

clf = svm.SVC(gamma ='scale')
def face_recognize(dir, test, pred):
    encodings = []
    names = []
    attendance = set()
    if pred == 1:
        test_image = face_recognition.load_image_file(test)

        # Find all the faces in the test image using the default HOG-based model
        face_locations = face_recognition.face_locations(test_image)
        no = len(face_locations)
        #print("Number of faces detected: ", no)

        # Predict all the faces in the test image using the trained classifier
        #print("Found:")
        for i in range(no):
            test_image_enc = face_recognition.face_encodings(test_image)[i]
            name = clf.predict([test_image_enc])
            attendance.add(*name)
        return attendance


    # Training the SVC classifier
    # The training data would be all the
    # face encodings from all the known
    # images and the labels are their names


    # Training directory
    if dir[-1]!='/':
        dir += '/'
    train_dir = os.listdir(dir)

    # Loop through each person in the training directory
    for person in train_dir:
        if 'DS_Store' in person:
            continue
        pix = os.listdir(dir + person)

        # Loop through each training image for the current person
        for person_img in pix:
            if 'DS_Store' in person_img:
                continue
            # Get the face encodings for the face in each image file
            face = face_recognition.load_image_file(
                dir + person + "/" + person_img)
            face_bounding_boxes = face_recognition.face_locations(face)

            # If training image contains exactly one face
            if len(face_bounding_boxes) == 1:
                face_enc = face_recognition.face_encodings(face)[0]
                # Add face encoding for current image
                # with corresponding label (name) to the training data
                encodings.append(face_enc)
                names.append(person)
            else:
                print(person + "/" + person_img + " can't be used for training")

    # Create and train the SVC classifier

    clf.fit(encodings, names)

    # Load the test image with unknown faces into a numpy array

    test_image = face_recognition.load_image_file(test)

    # Find all the faces in the test image using the default HOG-based model
    face_locations = face_recognition.face_locations(test_image)
    no = len(face_locations)
    #print("Number of faces detected: ", no)

    # Predict all the faces in the test image using the trained classifier
    #print("Found:")
    for i in range(no):
        test_image_enc = face_recognition.face_encodings(test_image)[i]
        name = clf.predict([test_image_enc])
        attendance.add(*name)
    return attendance

def main():
    curr = os.getcwd()
    train_dir =  curr + '/train_dir'
    test_image_before = curr + '/test_image_before.jpg'
    test_image_after  = curr + '/test_image_after.jpg'
    test_image_final = curr + '/test_image_final.jpg'

    roster_file = open(r"roster.txt")
    roster = []
    for item in roster_file:
        item = item.split(',')
        roster = item
    diff = utils.diffcalc(test_image_before, test_image_after)
    diff.save('test_image_final.jpg')
    before = face_recognize(train_dir, test_image_before, 0)
    after = face_recognize(train_dir, test_image_after, 1)
    final = face_recognize(train_dir, test_image_final, 1)
    attendance = set()
    absent = set()
    evaders = set()
    output_name = 'Attendace_Report' + str(datetime.now())[0:10] + '.txt'

    output = open(output_name,"a")
    output.write('Present:')
    output.write('\n')
    for item in before:
        if item in roster:
            attendance.add(item)
    for item in after:
        if item in roster:
            attendance.add(item)
    if len(attendance) == 0:
        output.write('None')
        output.write('\n')
    else:
        for item in attendance:
            output.write(item)
            output.write('\n')
    output.write('\n')
    output.write('Attendance Percentage:')
    output.write('\n')
    output.write(str((len(attendance)/len(roster)) * 100))
    output.write('\n')
    output.write('\n')
    output.write('Absent:')
    output.write('\n')
    for item in roster:
        if item not in attendance:
            absent.add(item)
    if len(absent) == 0:
        output.write('None')
        output.write('\n')
    else:
        for item in absent:
            output.write(item)
            output.write('\n')
    output.write('\n')
    output.write('Potential Evaders:')
    output.write('\n')
    for item in final:
        if item in roster:
            evaders.add(item)
    if len(evaders) == 0:
        output.write('None')
        output.write('\n')
    else:
        for item in evaders:
            output.write(item)
            output.write('\n')
    unknowns = max(len(before), len(after)) - len(roster)
    output.write('There are ' + str(unknowns) + ' unknown members in this call')
    output.write('\n')


if __name__=="__main__":
    main()
