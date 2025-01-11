import {useState} from "react";

const apiUrl = "http://127.0.0.1:5000"  // Accessing the environment variable

const useSubmitUrl = () => {
    const [loading, setLoading] = useState(false);
    const [malicious, setMalicious] = useState();
    const [error, setError] = useState(false);
    const [probability, setProbability] = useState(0);

    const checkUrl = async (url) => {
        try {
            setLoading(true);
            
            const response = await fetch(`${apiUrl}/predict_url`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({url: url}),
            });

            const data = await response.json();

            if (response.ok && data.prediction !== undefined && data.probability !== undefined) {
                setMalicious(data.prediction);
                setProbability(data.probability);
                }
            else {
                setError(true);
            }


        } catch (err) {
            console.log(err);
            setError(true);
        } finally {
            setLoading(false);
        }
    }

    return {loading, malicious, error, checkUrl, probability}
}

export default useSubmitUrl
