CV_scanner_app
🧠 AI CV Scanner (Automated Resume Analysis System)

The AI CV Scanner is a web-based system that allows users to upload their CVs (PDF/DOCX), which are then automatically analyzed by an AI model to extract key information and generate a score out of 100.

The project is designed to simplify and speed up the recruitment process by automating resume screening and candidate evaluation.

🚀 Features

✅ CV Upload (PDF/DOCX) through a simple web form

⚙️ Flask Backend that handles file uploads and communicates with workflows

🤖 n8n Workflow Automation running on AWS EC2 to orchestrate AI tasks

🧩 AI Model Integration (via Ollama) for smart CV parsing and scoring

📬 Email Notifications sent to HR once a valid CV is analyzed

☁️ AWS S3 Storage for securely saving uploaded files and results

🔄 Automatic Status Updates (scanning, analyzing, done) in the web interface

🧰 Tech Stack

Frontend: HTML, CSS, JavaScript (with real-time status updates)

Backend: Python (Flask)

Automation: n8n (running on AWS EC2)

Storage: AWS S3

AI Model: Ollama (Gemma:2b or other supported LLMs)

⚙️ How It Works

The user uploads a CV through the web interface.

Flask stores it in S3 and sends a webhook to n8n.

n8n triggers an AI model to analyze the CV content.

Once complete, the system updates the status and displays the AI-generated score and analysis.

HR (or the user) receives an email with the final result.

🧾 Future Enhancements

🧠 Improve AI model scoring logic

📊 Add detailed skill and experience extraction

💬 Add a chatbot to interactively review CV feedback

📈 Dashboard for recruiters to track submissions

👨‍💻 Author

Youssef Gammar Passionate about AI, automation, and cloud-based systems. 💼 Building intelligent tools to simplify everyday workflows.
