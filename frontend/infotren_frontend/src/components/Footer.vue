<template> 
    <footer>
        <div class="footer-form_row">
            <div class="footer-from_col">
                <img src="" class="footer-logo">
            </div>
            <div class="footer-col">
                <h3>Office</h3>
                <p>Strada Garii nr 4</p>
                <p>Bucuresti, jud Bucuresti, 79009</p>
                <p class="footer-email-id">cfr@gmail.com</p>
                <h4>+40 741983790</h4>
            </div>
            <div class="footer-col">
                <h3>Links</h3>
                <ul>
                    <li><a href="">Home</a></li>
                    <li><a href="">Buy Ticket</a></li>
                    <li><a href="">About Us</a></li>
                    <li><a href="">Q&A</a></li>
                    <li><a href="">Contact</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h3>Newsletter</h3>
                <form>
                    <input type="email" placeholder="Enter your email id" required>
                </form>
            </div>
        </div>
    </footer>
</template>

<script>
export default {
    name: "Footer"
};
</script>

<style scoped>
footer {
    width: 100%;
    position: fixed; /* Changed to fixed to ensure it stays at the bottom */
    bottom: 0; /* Stick to the bottom of the viewport */
    background: linear-gradient(to right, #00083c, #2d0b00); /* Ensure background color is set */
    color: #fff;
    padding: 50px 0 10px;
    font-size: 13px;
    line-height: 10px;
    z-index: 1000; /* Ensure it stays above other content */
}

.footer-form_row {
    width: 68%;
    margin: auto;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    justify-content: space-between;
}

.footer-from_col {
    flex-basis: 25px;
}

.footer-logo {
    width: 80px;
    margin-bottom: 30px;
}

.footer-col h3 {
    width: fit-content;
    margin-bottom: 40px;
    position: relative;
}

.footer-email-id {
    width: fit-content;
    border-bottom: 1px solid #ccc;
    margin: 20px 0;
}

.footer-col ul li {
    list-style: none;
    margin-bottom: 12px;
}

.footer-col ul li a {
    text-decoration: none;
    color: #fff;
}

footer form {
    padding-bottom: 15px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #ccc;
    margin-bottom: 50px;
}

footer form input {
    width: 100px;
    background: transparent;
    color: #ccc;
    border: 0;
}
</style>
