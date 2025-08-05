terraform {
  required_providers {
    docker = {
        source = "kreuzwerker/docker"
        version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host = "tcp://192.168.100.200:2375/"
}

# Network
resource "docker_network" "app_network" {
  name = "app_network"
  #driver = "bridge"
}

# Images
resource "docker_image" "web" {
    name = "rabitor/web1:v1.0"
    keep_locally = false
}

resource "docker_image" "db" {
    name = "rabitor/db:latest"
    keep_locally = false
}

# Containers
resource "docker_container" "db_container" {
    name = "db"
    image = docker_image.db.image_id      
    
    networks_advanced {
        name = docker_network.app_network.name
    }
    
    env = [
        "MYSQL_ROOT_PASSWORD=12345"    
    ]
}

resource "docker_container" "web_container" {
    name = "web"
    image = docker_image.web.image_id
    ports {
      internal = 80
      external = 8080
    }

  networks_advanced {
    name = docker_network.app_network.name
  }
  depends_on = [ docker_network.app_network, docker_container.db_container ]    
}

