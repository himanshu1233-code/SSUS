import streamlit as st
import pandas as pd

from database.mongodb import students_collection, attendance_collection

st.title("Attendance Management")

students = list(students_collection.find())

if not students:
    st.warning("No students found. Please register students first.")
    st.stop()

student_dict = {
    f"{student['first_name']} {student['last_name']}": student["_id"]
    for student in students
}

selected_student = st.selectbox("Select Student", list(student_dict.keys()))

attendance_date = st.date_input("Attendance Date")

status = st.selectbox("Attendance Status", ["Present", "Absent"])

if st.button("Mark Attendance"):

    existing = attendance_collection.find_one({
        "student_name": selected_student,
        "date": str(attendance_date)
    })

    if existing:
        st.warning("Attendance already marked for this date.")
    else:
        attendance_collection.insert_one({
            "student_id": str(student_dict[selected_student]),
            "student_name": selected_student,
            "date": str(attendance_date),
            "status": status
        })
        st.success("Attendance marked successfully!")

st.subheader("Attendance Records")

records = list(attendance_collection.find({}, {"_id": 0}))

if records:
    st.dataframe(pd.DataFrame(records))
else:
    st.info("No attendance records found.")

st.subheader("Attendance Summary")

for student in student_dict.keys():

    total = attendance_collection.count_documents({
        "student_name": student
    })

    present = attendance_collection.count_documents({
        "student_name": student,
        "status": "Present"
    })

    percentage = (present / total * 100) if total > 0 else 0

    st.write(f"{student}: {percentage:.2f}%")