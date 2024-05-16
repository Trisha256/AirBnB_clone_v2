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