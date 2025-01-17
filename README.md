Description
This project involves building a Vue.js web application for Influencer Engagement & Sponsorship Coordination app. The application has three user roles: Admin and Sponsor and Influencer. Admin can accept, and reject new signed up sponsors and flag any user(sponsor or influencer) and any ad campaign . Sponsor can create, edit, delete ad campaign also can send ad Request to influencer for creating ad , can also negotiate with sponsor with chat. Influencer can edit their profile , can send ad request for a campaign, can create ad for the campaign, negotiate for an ad request.
Technologies used
    ● Vue.js: A JavaScript framework for building user interfaces. It allows for creating dynamic and responsive web applications with its component-based architecture.
    ● BootstrapVue: A library that integrates Bootstrap components with Vue.js, providing a convenient way to create visually appealing and responsive user interfaces.
    ● Vue Router: A routing library for Vue.js applications. It enables navigation between different views and components in a single-page application.
    ● Axios: A popular HTTP client for making asynchronous HTTP requests. It's used to communicate with the backend API to fetch and send data.
    ● Flask: A lightweight and flexible Python web framework. It's used to build the backend API that handles data storage, retrieval, and manipulation.
    ● Flask-CORS: An extension for handling Cross-Origin Resource Sharing (CORS) in Flask applications. It allows the frontend to make requests to the backend from a different domain.
    ● SQLAlchemy: A powerful SQL toolkit and Object-Relational Mapping (ORM) library for Python. It's used to interact with the database and manage database operations.
    ● SQLite: A lightweight, serverless, and self-contained database engine. It's used as the database system to store and manage application data.
    ● JWT (JSON Web Tokens): A compact and self-contained way for securely transmitting information between parties as a JSON object. It's used for user authentication and authorization.
    ● Python: The programming language used for developing the Flask backend and handling server-side logic.
API Design
I have used normal api design. All database tables have CRUD operations available through the API. Authentication tokens are used for specific requests that require them. These tokens can only be obtained from the user's account page when signed in.
Architecture and Features
The architecture of the app follows a client-server model, where Vue.js serves as the frontend framework and Python-Flask as the back-end framework. Vue.js handles the presentation layer and manages user interactions through its MVVM architecture, while Python-Flask handles the server-side logic, such as HTTP requests and responses, asynchronous tasks, and database interactions.
The features of the application are as follows:
    ● User authentication: Signup and Login.
    ● Sponsor can add, delete, edit campaign , search for influencer , send ad request to influencer, can receive ad request from influencer.
    ● Influencer can view all campaign , search for campaign, send and receive ad request .
    ● Sponsor can edit ad request , delete send ad request, negotiate received and send ad request .
    ● Influencer can delete send ad request, negotiate send and received ad request.
    ● Admin can flag any user or campaign. Also accept or reject newly created sponsor.
    ● User-specific API tokens: Generate tokens to use user-specific requests
    ● Reminders: Influencer Receive daily reminder for Influencer.
    ● Monthly report for sponsor .

video link : https://drive.google.com/file/d/1vKKBFkkDzB8NRDA1Lj2x4eD7N5ijXakq/view?usp=sharing
