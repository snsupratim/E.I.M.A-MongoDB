from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient('mongodb+srv://nagsupratim8:cmXzynT1ANQMufEe@cluster0.ksv5a.mongodb.net/knowledge_base?retryWrites=true&w=majority&appName=Cluster0')
db = client['knowledge_base']
collection = db['responses']

# Data to Insert
data = [
    {"text": "The library is open from 8 AM to 10 PM on weekdays and 10 AM to 6 PM on weekends."},
    {"text": "You can access the e-library by logging into the student portal with your college credentials."},
    {"text": "The next semester starts on January 15th."},
    {"text": "The grading policy is based on a 10-point CGPA system with grades ranging from O (Outstanding) to F (Fail)."},
    {"text": "You can apply for re-evaluation through the student portal under the 'Examinations' section."},
    {"text": "The hostel fees are ₹50,000 per semester, including accommodation and meals."},
    {"text": "You need to log in to the student portal, fill in your course preferences, and pay the semester fees."},
    {"text": "The academic calendar is available on the college website under the 'Academics' section."},
    {"text": "You can join a student club by attending their orientation sessions or contacting the club coordinator."},
    {"text": "Yes, scholarships are available based on merit and financial need. Check the 'Scholarships' section on the college website."},
    {"text": "Placement drives are scheduled from February to April. Keep an eye on the placement portal for updates."},
    {"text": "The attendance requirement is 75% for each subject to be eligible for exams."},
    {"text": "You can contact your professors via email or during their office hours, listed on the department notice board."},
    {"text": "The dining hall is open from 7 AM to 9 PM, with specific slots for breakfast, lunch, and dinner."},
    {"text": "Tuition fees can be paid online through the student portal or at the accounts office."},
    {"text": "Yes, there is a fully-equipped gym on campus open from 6 AM to 9 PM."},
    {"text": "You can get a student ID card from the administration office after completing your registration."},
    {"text": "You can request a transcript through the student portal under the 'Academics' section."},
    {"text": "Use your student credentials to log in to the campus Wi-Fi network."},
    {"text": "The cultural fest is scheduled for March 20th to 22nd."},
    {"text": "Yes, you can apply for part-time jobs on campus through the career services office."},
    {"text": "Submit a leave application form through the student portal or directly to your department office."},
    {"text": "Submit your internship details to the placement office for approval."},
    {"text": "Past exam papers are available in the library or the student portal under 'Resources'."},
    {"text": "You can update your contact details through the student portal under the 'Profile' section."},
    {"text": "Fill out the hostel application form available on the student portal."},
    {"text": "You need a CGPA of 9.0 or above and no disciplinary records to qualify for the Dean's List."},
    {"text": "You can check your attendance on the student portal under the 'Attendance' section."},
    {"text": "The refund policy is detailed in the student handbook under the 'Fees' section."},
    {"text": "The midterm exams are scheduled for October 10th to 15th."},
    {"text": "Contact your department head or a faculty member working in your area of interest."},
    {"text": "Yes, there is a mentoring program. You can sign up through the student portal."},
    {"text": "Seminar rooms can be booked through the facilities management office."},
    {"text": "The campus has facilities for cricket, football, basketball, badminton, and tennis."},
    {"text": "The convocation ceremony is scheduled for November 25th."},
    {"text": "Workshop registrations are available on the events section of the student portal."},
    {"text": "You can apply for a bonafide certificate through the administration office or student portal."},
    {"text": "Information about electives is available in the course catalog on the student portal."},
    {"text": "Apply through the international relations office with your academic and extracurricular records."},
    {"text": "Yes, coding contests are organized every semester by the computer science department."},
    {"text": "Visit the campus health center for any medical assistance."},
    {"text": "The syllabus is available on the student portal under 'Academics'."},
    {"text": "Assignments can be submitted through the LMS or directly to your professor."},
    {"text": "Submit a course withdrawal form through the student portal."},
    {"text": "Yes, the college offers language courses in French, Spanish, and German."},
    {"text": "Report lost items to the security office or the lost and found section."},
    {"text": "Consult with your academic advisor and submit a major change form."},
    {"text": "Exam results will be declared two weeks after the exams."},
    {"text": "Visit the administration office to request a reissue of your ID card."},
    {"text": "Register for sports events through the sports department or student portal."},
    {"text": "The release date of the 6th semester exam is January 26th."},
    {"text": "The result of the 5th semester will be declared on February 15th."},
    {"text": "6th semester exam date is 20 December."},
    {"text": "7th semester exam date is 22 December."},
    {"text": "8th semester exam date is 23 December."},
    {"text": "Pragati event will be in January."},
    {"text": "Spectra event will be in March."},
    {"text": "Brainrush event will be in April."},
    {"text": "Dataquest event will be in May."},
    {"text": "Insignia event will be in October."},
    {"text": "The release date for the annual cultural fest is February 10th."},
    {"text": "The fee submission deadline for the 6th semester is January 15th."},
]

# Insert data into the MongoDB collection
collection.insert_many(data)

print("Data inserted successfully!")
