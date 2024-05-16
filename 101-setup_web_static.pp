# Define the class for web server setup
class web_server_setup {
  # Install Apache
  package { 'apache2':
    ensure => installed,
  }

  # Start and enable Apache service
  service { 'apache2':
    ensure => running,
    enable => true,
  }

  # Create web_static directory
  file { '/var/www/html/web_static':
    ensure => directory,
    owner  => 'www-data',
    group  => 'www-data',
    mode   => '0755',
  }

  # Create index.html file
  file { '/var/www/html/index.html':
    ensure  => file,
    owner   => 'www-data',
    group   => 'www-data',
    mode    => '0644',
    content => 'Hello, World!',
  }
}

# Apply the web_server_setup class to your web servers
node 'web-01', 'web-02' {
  include web_server_setup
}
# configuration of an nginx web server
exec { 'apt-get-update':
  command => '/usr/bin/env apt-get -y update',
}
-> exec {'test folder':
  command => '/usr/bin/env mkdir -p /data/web_static/releases/test/',
}
-> exec {'nginx':
  command => '/usr/bin/env apt-get -y install nginx',
}
-> exec {'shared folder':
  command => '/usr/bin/env mkdir -p /data/web_static/shared/',
}
-> exec {'index':
  command => '/usr/bin/env echo "Welcome to AirBnB" > /data/web_static/releases/test/index.html',
}
-> exec {'ln -s':
  command => '/usr/bin/env ln -sf /data/web_static/releases/test /data/web_static/current',
}
-> exec {'nginx conf':
  command => '/usr/bin/env sed -i "/listen 80 default_server/a location /hbnb_static/ { alias /data/web_static/current/;}" /etc/nginx/sites-available/default',
}
-> exec {'chown:':
  command => '/usr/bin/env chown -R ubuntu:ubuntu /data',
}
-> exec {'service':
  command => '/usr/bin/env service nginx restart',
}
