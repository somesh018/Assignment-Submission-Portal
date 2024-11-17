# Assignment Submission Portal

This is a backend system for an assignment submission portal where users can upload assignments and admins can manage them.

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set up MongoDB (ensure MongoDB is running on localhost).

3. Set up environment variables in a `.env` file (optional).

4. Run the app:
    ```bash
    python main.py
    ```

## API Endpoints

### User Endpoints

- `POST /user/register`: Register a new user.
- `POST /user/login`: User login.
- `POST /user/upload`: Upload an assignment.
- `GET /user/admins`: Get a list of admins.

### Admin Endpoints

- `POST /admin/login`: Admin login.
- `GET /admin/assignments`: View assignments.
- `POST /admin/assignments/<id>/accept`: Accept an assignment.
- `POST /admin/assignments/<id>/reject`: Reject an assignment.
