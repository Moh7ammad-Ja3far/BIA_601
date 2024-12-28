document.getElementById('scheduleForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const clinicName = document.getElementById('clinic-name').value;
    const numDoctors = document.getElementById('numDoctors').value;
    const numPatients = document.getElementById('numPatients').value;
    const appointmentDuration = document.getElementById('appointmentDuration').value;

    const response = await fetch('/schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            clinic_name: clinicName,
            num_doctors: numDoctors,
            num_patients: numPatients,
            appointment_duration: appointmentDuration
        })
    });

    const result = await response.json();
    displaySchedule(result);
});

function displaySchedule(result) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = ''; 
    if (result.schedule && result.schedule.length > 0) {
        result.schedule.forEach(appointment => {
            const appointmentElement = document.createElement('p');
            appointmentElement.textContent = `Clinic Name ${appointment.clinic} - Doctor ${appointment.doctor}: Patient ${appointment.patient} - ${appointment.time}`;
            resultsDiv.appendChild(appointmentElement);
        });
    } else {
        resultsDiv.textContent = 'No appointments available.';
    }
}
