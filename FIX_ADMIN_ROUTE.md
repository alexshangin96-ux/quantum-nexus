# Fix Admin Route 404 Error

The `/admin` route returns 404 because Nginx is not configured to proxy it to Flask.

## Solution

On the server, edit the Nginx configuration:

```bash
sudo nano /etc/nginx/sites-available/quantum-nexus
```

Add this location block for the admin route:

```nginx
location /admin {
    proxy_pass http://127.0.0.1:5000/admin;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Then reload Nginx:

```bash
sudo systemctl reload nginx
```

Or use the direct URL with the port:

```bash
https://quantum-nexus.ru:5000/admin
```






