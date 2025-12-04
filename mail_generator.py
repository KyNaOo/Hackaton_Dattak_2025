import requests
import json

def generate_email(subject, details, company, name, sendername="John Doe", tone="professional"):
    """
    Generate email using local Ollama instance
    Make sure Ollama is running and you've pulled a model (e.g., 'ollama pull phi')
    """
    
    prompt = f"""Write a {tone} email with these exact details:

Subject: {subject}
Recipient: {name} at {company}
Message: {details}
Sender: {sendername}

Write ONLY the email body (no subject line, no placeholders):"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                "model": "phi", 
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 250 
                }
            },
            timeout=60  
        )
        
        response.raise_for_status()
        result = response.json()
        return result['response'].strip()
        
    except requests.exceptions.ConnectionError:
        return "Error: Ollama is not running. Start it with 'ollama serve' or launch the Ollama app."
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    subject = "Meeting Rescheduling"
    details = "I need to move our meeting from Wednesday to Friday at 3 PM because of a conflict."

    print("Generating email...")
    email = generate_email(subject, details, "Amazon", "GMK")
    print("\nGenerated Email:\n")
    print(email)