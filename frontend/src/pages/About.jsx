import React from 'react'

const About = () => {
  return (
    <div>
        <div className="container mx-auto p-4 mt-8 max-w-3xl">
    
        <h1 className="text-3xl font-bold text-center text-blue-600">About This Website</h1>
        
        <div className="container p-6">        
            <p className="text-center mt-4 text-gray-700">This website was made out of the kaggle dataset shown here: 
                <a href="https://www.kaggle.com/datasets/shashwatwork/phishing-dataset-for-machine-learning" className="text-blue-500 hover:text-blue-700"> Phishing Website Dataset</a>. 
                The model used to classify the websites is a Logistic Regression model. The model was trained on the dataset and then deployed using Flask and React. The frontend was made using React and Tailwind CSS. 
                The code for this website can be found here: <a href="https://colab.research.google.com/drive/1PEUx_5g7xRI5RkcvffeyYdsYpRFmHMon" className="text-blue-500 hover:text-blue-700">Google Colab Notebook</a>
            </p>
        </div>
        </div>
    </div>
  )
}

export default About
