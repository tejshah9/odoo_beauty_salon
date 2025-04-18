# 💇‍♀ Odoo Beauty Salon Module

A feature-rich custom Odoo 18 module built for managing all aspects of a modern beauty salon — from customers and appointments to services, staff, and packages. Designed with efficiency, simplicity, and scalability in mind.

---

## ✨ Features

- *📅 Appointment Calendar*  
  Schedule and manage appointments with real-time visibility of slots, services, and assigned staff.

- *👥 Customer Management*  
  Keep track of customer details, history, and their preferences. View all related appointments and packages from one place.

- *💆 Services Catalog*  
  Define and manage all salon services like haircuts, facials, massages, etc. with pricing and duration.

- *🎁 Packages*  
  Create attractive service bundles with discounted pricing and assign them to customers.

- *🧑‍🔧 Staff Management*  
  Maintain staff profiles and link them with appointments and services they provide.


---

## 🔗 Model Relationships

This module uses smart relationships between models:

- A *Customer* can have multiple *Appointments*
- An *Appointment* is linked with:
  - One *Customer*
  - One or more *Services*
  - One *Staff* member
- A *Package* can include multiple *Services*
- Customers can be assigned to *Packages*

---

## 🧠 Tech Stack

- *Odoo Version:* 18
- *Language:* Python
- *Framework:* Odoo ORM, XML
- *Views:* Form, Tree, Kanban, Calendar

---

