import React from 'react'

const About = () => {
  return (
    <div>
        <div className="container mx-auto p-4 mt-10">
    
        <h1 className="text-3xl font-bold text-center">About This Website</h1>
        <p className="text-center mt-4">This website was made out of the kaggle dataset shown here: 
            <a href="https://www.kaggle.com/datasets/shashwatwork/phishing-dataset-for-machine-learning">Phishing Website Dataset</a>. 
 The model used to classify the websites is a Logistic Regression model. The model was trained on the dataset and then deployed using Flask and React. The frontend was made using React and Tailwind CSS. 
 The code for this website can be found here:  </p>
        </div>
    </div>
  )
}

export default About
