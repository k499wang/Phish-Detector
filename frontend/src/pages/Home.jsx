import React from 'react'
import { useState } from "react";
import { FloatingLabel } from "flowbite-react";
import useSubmitUrl from "../hooks/useSubmitUrl";
import Popup from 'reactjs-popup';
import Spinner from "../components/Spinner";

const Home = () => {
    const [url, setUrl] = useState("");
    const [enter, setEnter] = useState(false);
    const [valid, setValid] = useState(false);
    const [popup, setPopup] = useState(false);

    const {loading, malicious, error, checkUrl, probability} = useSubmitUrl();

    const handleChange = (e) => {
        // Handle input change and validate URL
        e.preventDefault();
        setUrl(e.target.value);
        setEnter(true);

        try {
            new URL(e.target.value); // validate URL
            setValid(true);
        } catch {
            setValid(false);
        }
    };

    const handlePaste = (e) => {
        // Handle paste event and validate URL after paste
        const pastedText = e.clipboardData.getData("text");
        setUrl(pastedText);
        setEnter(true);

        try {
            new URL(pastedText); // validate pasted URL
            setValid(true);
        } catch {
            setValid(false);
        }
    };

    const handleSubmit = async () => {
        console.log("URL submitted: ", url);
        if (valid) {
            
            console.log("Valid URL");
            await checkUrl(url);

            if (error) {
                alert("Invalid URL, Cannot Access. Try checking if the website is up or not.");
                return;
            }

            setPopup(true);
        } else {
            console.log("Invalid URL");
            alert("Please enter a valid URL.");
        }
    };

    return (
        <div className="container mx-auto p-4 mt-10">
            <h1 className="text-3xl font-bold text-center">Check for Phishing Websites Using Machine Learning</h1>
            <p className="text-center mt-4">Enter a URL below to check if it is a phishing website. This uses a Logistic Regression model to classify websites as malicious or not. Please enter a Valid URL.</p>
            <div className="container bg-white p-4 rounded-lg shadow-lg mt-4">
                <FloatingLabel
                    variant="filled"
                    label="Enter URL..."
                    helperText="Please enter a valid URL."
                    onChange={handleChange}
                    onPaste={handlePaste} // Add paste handler here
                    autoComplete="off"
                />
            </div>

            <div className="relative flex justify-center mt-4">
                {/* Loading spinner positioned absolutely */}
                {loading && (
                    <div className="absolute inset-0 flex justify-center items-center bg-gray-100 bg-opacity-50 z-50">
                        <Spinner />
                    </div>
                )}
            </div>

            {enter && !valid && (
                <p className="text-red-500 mt-2">Please enter a valid URL.</p>
            )}

            <Popup open={popup && !error} closeOnDocumentClick onClose={() => setPopup(false)}>
                <div className="container mx-auto p-4 mt-10 bg-white rounded-lg shadow-lg">
                    <h1 className="text-3xl">Results</h1>
                    <p className="flex popup-probability mt-4">Probability: {probability}</p>
                    <p className="flex mt-1">
                        {(malicious === 1) ? 'This URL is potentially malicious!' : 'This URL seems safe.'}
                    </p>

                    <div className="flex justify-center">
                        <button type="button" onClick={() => setPopup(false)} className="text-gray-900 mt-2 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 font-medium rounded-full text-sm px-5 py-2.5 me-2 mb-2 dark:bg-gray-800 dark:text-white dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700">Exit</button>
                    </div>
                </div>
            </Popup>

            {loading && (
                <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
                </div>
            )}

            <div className="flex justify-center mt-4">
                <button type="button" className="py-2.5 px-5 me-2 mb-2 text-sm font-medium text-gray-900 focus:outline-none bg-white rounded-lg border border-gray-200 hover:bg-gray-100 hover:text-blue-700 focus:z-10 focus:ring-4 focus:ring-gray-100 dark:focus:ring-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:border-gray-600 dark:hover:text-white dark:hover:bg-gray-700" onClick={handleSubmit}>
                    Submit
                </button>
            </div>
        </div>
    );
};

export default Home;
