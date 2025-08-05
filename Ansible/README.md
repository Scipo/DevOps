# Vagrant & Ansible Multi-OS Infrastructure Setup

Infrastructure Diagram

This project demonstrates how to create a multi-OS infrastructure environment using:
- **Vagrant** for virtualization
- **Ansible** for configuration management

## 🖥️ Infrastructure Overview

| Host | OS        | Role          | Software Stack          |
|------|-----------|---------------|-------------------------|
| `web`| Debian    | Web Server    | Apache + PHP      |
| `db` | AlmaLinux | Database Server| MySQL/MariaDB          |

## ✨ Key Features

- **Multi-OS Environment**: Debian and AlmaLinux hosts working together
- **Automated Provisioning**: Fully configured with Ansible playbooks
- **Network Connectivity**: Hosts communicate via private network
- **Role Separation**: Clear web and database server roles

## 🚀 Getting Started

### Prerequisites

- [Vagrant](https://www.vagrantup.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (or other supported provider)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html)

