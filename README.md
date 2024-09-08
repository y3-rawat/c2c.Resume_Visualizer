
# Resume Analysis System

This project consists of two main components: a resume upload interface and a resume analysis API. It's designed to allow users to upload resumes and receive automated analysis.

## Project Structure

- `resume_upload/`: Frontend for resume upload
- `resume_test_api/`: Backend API for resume analysis
- `run.py`: Script to set up and run the entire system

### Resume Upload (Frontend)

Located in the `resume_upload/` directory:

- `index.html`: Main page for resume upload
- `loader.html`: Loading page at start 
- `result.html`: Page to display analysis results
- `api/upload.js`: Handles file upload functionality

- `README.md`: Specific instructions for the frontend
- `vercel.json`: Configuration for Vercel deployment

### Resume Test API (Backend)

Located in the `resume_test_api/` directory:

- `app.py`: Flask application for resume analysis

## Setup and Running

1. Ensure you have Python and Node.js installed on your system.
2. Clone this repository to your local machine.
3. Run the `run.py` script:

   ```python
   python run.py
   ```

   This script will:
   - Check for and install necessary dependencies
   - Start the Python backend server
   - Start the Node.js frontend server
   - Open the application in your default web browser

## Usage

1. Open the application in your web browser (should happen automatically after running `run.py`).
2. Upload a resume, job description, company name, position name , groq api key using the interface and click on the "Analyze" button.
3. Wait for the analysis to complete.
4. View the analysis results on the results page.

## Development

- Frontend: The resume upload interface is built with HTML, CSS, and JavaScript.
- Backend: The resume analysis API is built with Python using Flask.


## Deployment

The frontend and backend are deployed in render. Top layer is deployed on vercel here [c2c-resume-visual](https://c2c-resume-visual.vercel.app/)
## Contributing

Contributions to improve the project are welcome. Please feel free to submit issues and pull requests.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

