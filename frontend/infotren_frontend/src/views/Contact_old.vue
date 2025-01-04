<template>
    <div class="form-page">
<div class="contact-container">
    <form action=" " class="contact=left">
        <div class="contact-left-title">

            <h2>Get in touch</h2>
            <hr>
        </div>
        <input type="text" name="name" placeholder="Your Name" class="contact-inputs" required>
        <input type="email" name="email" placeholder="Your Email" class="contact-inputs" required>
       <textarea name="message" placeholder="Your Message" class="contact-inputs" required></textarea>
       <button type="submit">Submit <img src="" alt=""></button>
    </form>
    <div class="contact-right">
    <img src="../assets/tren1.jpg" alt="" width="600" height="500">

</div>
    </div>
</div>

    
</template>

<style>

.form-page * {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

.form-page  {
  font-family: 'Outfit';
  background: linear-gradient(#ffdad5, #fff7f9);
}

.form-page .contact-container {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: space-evenly;
}

.form-page .contact-left {

  display: flex;
  flex-direction: column;
  align-items: start;
  gap:20px;
}
.form-page .contact-left-title h2 {
  font-weight: 600;
  color:#a363aa;
  font-size: 40px;
  margin-bottom: 5px;
}

.form-page .contact-left-title hr {
  border:none;
  width: 120px;
  height: 5px;
  background-color: #a363aa;
  border-radius: 10px;
  margin-bottom: 20px;
}
.form-page .contact-right {
  display: flex;
  flex-direction: column;
  align-items: start;
  gap:20px;
}

.form-page .contact-inputs {
  width: 400px;
  height: 50px;
  border:none;
  outline:none;
  padding-left: 25px;
  font-weight: 500;
  color: #666;
  border-radius: 50px;
}
.form-page .contact-left textarea {

  height: 140px;
  padding-top: 15px;
  border-radius:20px;
  padding-left: 25px;
}
.form-page .contact-inputs:focus{
border: 2px solid #ff994f;
}

.form-page .contact-inputs:focus{
border: 2px solid #ff994f;
}

.form-page .contact-inputs:placeholder{
color: #a9a9a9;
}

.form-page .contact-left:button{
display: flex;
align-items: center;
padding: 15px 30px;
font-size: 16px;
color: #fff;
gap: 10px;
border:none;
border-radius:50px;
background: linear-gradient(270deg, #ff994f, #fa6d86);
cursor:pointer;
}

.form-page .contact-left button img{
    height: 15px;
}

.form-page .contact-right img{
    width: 500px;
}

@media (max-width:800px){
    .form-page .contact-inputs{
        width: 80vw;
    }
    .form-page .contact-right{
        display:none;
    }
}

</style>