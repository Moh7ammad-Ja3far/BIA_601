from flask import Flask, render_template, request, session, redirect, url_for
from main import GeneticAlgorithm

app = Flask(__name__)
app.secret_key = "xkey"

@app.route("/", methods=["GET", "POST"])
def Step1():
    if request.method == "POST":
        DoctorsNumber = int(request.form["DoctorsNumber"])
        if DoctorsNumber <= 0 or DoctorsNumber > 10:
            return "Error: Number of doctors must be between 1 and 10."
        session["DoctorsNumber"] = DoctorsNumber
        session["DoctorCapacities"] = []
        return redirect(url_for("Step2"))
    return render_template("step1.html")

@app.route("/step2", methods=["GET", "POST"])
def Step2():
    DoctorCapacities = session.get("DoctorCapacities", [])
    DoctorsNumber = session.get("DoctorsNumber", 0)
    if request.method == "POST":
        Capacity = int(request.form["Capacity"])
        if Capacity <= 0:
            return "Error: Doctor capacity must be greater than zero."
        DoctorCapacities.append(Capacity)
        session["DoctorCapacities"] = DoctorCapacities
        if len(DoctorCapacities) == DoctorsNumber:
            return redirect(url_for("Step3"))
    CurrentDoctor = len(DoctorCapacities) + 1
    return render_template("step2.html", CurrentDoctor=CurrentDoctor)

@app.route("/step3", methods=["GET", "POST"])
def Step3():
    if request.method == "POST":
        PatientsNumber = int(request.form["PatientsNumber"])
        if PatientsNumber <= 0:
            return "Error: Number of patients must be greater than zero."
        session["PatientsNumber"] = PatientsNumber
        return redirect(url_for("Result"))
    return render_template("step3.html")

@app.route("/result")
def Result():
    DoctorsNumber = session.get("DoctorsNumber")
    DoctorCapacities = session.get("DoctorCapacities")
    PatientsNumber = session.get("PatientsNumber")
    Schedule, UnscheduledPatients = GeneticAlgorithm(PatientsNumber, DoctorsNumber, DoctorCapacities)
    Result = {f"Doctor {i+1}": [] for i in range(DoctorsNumber)}
    for Patient, Doctor in enumerate(Schedule):
        Result[f"Doctor {Doctor+1}"].append(f"Patient {Patient+1}")
    return render_template(
        "result.html",
        Result=Result,
        UnscheduledPatients=[f"Patient {p+1}" for p in UnscheduledPatients]
    )
if __name__ == "__main__":
    app.run(debug=True)
