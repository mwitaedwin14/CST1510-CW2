#Week 7: Secure Authentication System

Student Name: Edwin Mwita
Student ID: M01036583
Course: CST1510-CW2- Multi-Domain Intelligence Platform

##Project Description

A command line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass

#Features

- Secure password hashing using bcrypt with automatic salt generation
- User registeration with duplicate username protection
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

##Technical implementation

-Hashing Algorithm: bcrypt with automatic salting 
-Data Storage: Plain text file ('users.txt') with comma-separated values 
-Password Security: One-way hashing, no plaintext storage 
-Validation: Username (3-20 alphanumeric characters), Password(6-50 characters)
