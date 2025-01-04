<template>
  <section id="about" class="about-wrapper">
    <div class="about-1">
      <h1>About Us</h1>
      <p>
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
        when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
        It has survived not only five centuries, but also the leap into electronic typesetting, 
        remaining essentially unchanged. 
      </p>
    </div>
    <div id="about-2" class="about-cards">
      <div class="content-box-lg container">
        <div class="row">
          <div class="col-md-4">
            <div class="about-item text-center">
              <i class="fa fa-book"></i>
              <h3>MISSION</h3>
              <hr />
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do 
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="about-item text-center">
              <i class="fa fa-eye"></i>
              <h3>VISION</h3>
              <hr />
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do 
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="about-item text-center">
              <i class="fa fa-heart"></i>
              <h3>VALUES</h3>
              <hr />
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do 
                eiusmod tempor incididunt ut labore et dolore magna aliqua.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>


<style scoped>
/* General Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Section Wrapper */
.about-wrapper {
  background-color: dimgray;
  color: white;
  padding: 50px 0; /* Adds spacing at top and bottom */
  width: 100%;
}

/* About Us Header */
.about-1 {
  text-align: center;
  padding: 20px;
  max-width: 900px;
  margin: 0 auto;
}

.about-1 h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 15px;
}

.about-1 p {
  font-size: 1.1rem;
  line-height: 1.8;
  margin: 0 15px;
}

/* Card Section */
.about-cards {
  
  padding: 50px 0;
  color: #333;
}

.about-item {
  background-color: #f9f9f9;
  padding: 30px 20px;
  margin: 15px 0;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.about-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  background-color: #5fbff9;
  color: #fff;
}

.about-item i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: #5fbff9;
}

.about-item h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.about-item hr {
  width: 50px;
  height: 3px;
  background-color: #5fbff9;
  border: none;
  margin: 0 auto 15px;
}

.about-item p {
  font-size: 1rem;
  line-height: 1.6;
}
</style>
