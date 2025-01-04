<template>
    <div class="contact-in">
        <div class="contact-map">
            <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d5696.708064248912!2d26.069430117476053!3d44.446411233819326!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40b201fca9df7749%3A0x7f1c3852fc0ea577!2sNorth%20Railway%20Station%20Neighborhood%2C%20Bucharest!5e0!3m2!1sen!2sro!4v1734178163911!5m2!1sen!2sro" width="100%" height="auto" style="border:0;" allow="fullscreen" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
        </div>
        <div class="contact-form">
            <h1>Contact Us</h1>
            <form action="https://api.web3forms.com/submit" method="POST">
                <input type="hidden" name="access_key" value="792e7818-b973-4e9e-b589-76fef508aa12">
                <input type="text" name="name" placeholder="Name" class="contact-form-txt" required />
                <input type="email" name="email" placeholder="Email" class="contact-form-txt" required />
                <textarea name="message" placeholder="Message" class="contact-form-txtarea" required></textarea>
                <input type="submit" placeholder="Submit" class="contact-form-btn" />
            </form>
        </div>
    </div>
</template>

<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    width: 100%;
    height: 100vh;
    display: grid;
    align-items: center;
    background: #8e2de2;
}

.contact-in {
    width: 80%;
    height: auto;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
    padding: 10px;
    border-radius: 10px;
    background: #fff;
    box-shadow: 0px 0px 0px 0px #666;
}

.contact-map {
    flex: 1;
    min-width: 300px; /* Ensure it doesn't get too small */
    height: auto;
    margin-bottom: 20px; /* Add space between map and form */
}

.contact-map iframe {
    width: 100%;
    height: 100%;
}

.contact-form {
    flex: 1;
    min-width: 300px;
    height: auto;
    padding: 30px;
    text-align: center;
}

.contact-form h1 {
    margin-bottom: 20px;
}

.contact-form-txt,
.contact-form-txtarea {
    width: 100%; /* Make the inputs take up full width */
    max-width: 500px; /* Optional: limit max width */
    height: 40px;
    color: #000;
    border: 1px solid #bcbcbc;
    border-radius: 50px;
    outline: none;
    margin-bottom: 20px;
    padding: 15px;
}

.contact-form-txtarea {
    height: 130px; /* More space for the message textarea */
}

.contact-form-txtarea::placeholder {
    color: #aaa;
}

.contact-form-btn {
    width: 100%;
    border: none;
    outline: none;
    border-radius: 50px;
    background: #822de2;
    color: #fff;
    text-transform: uppercase;
    padding: 10px 0;
    cursor: pointer;
    font-size: 18px;
}

.contact-form-btn:hover {
    background: #5f1db1; /* Change to a darker shade when hovered */
}

/* Responsive Design */
@media (max-width: 768px) {
    .contact-in {
        flex-direction: column; /* Stack map and form on smaller screens */
    }

    .contact-form {
        padding: 20px; /* Reduce padding on small screens */
    }
}
</style>
