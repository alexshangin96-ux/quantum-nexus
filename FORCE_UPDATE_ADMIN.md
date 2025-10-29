# Force Update Admin Panel

Выполните на сервере:

```bash
cd /root/quantum-nexus
git fetch origin
git reset --hard origin/main
git clean -fd
sudo cp admin.html /var/www/quantum-nexus/
sudo chown www-data:www-data /var/www/quantum-nexus/admin.html
sudo systemctl restart quantum-nexus-web
sudo systemctl status quantum-nexus-web
```

Проверьте обновление:
```bash
head -20 /var/www/quantum-nexus/admin.html | grep "value=\"smartfixnsk\""
```

Если видите "value=\"smartfixnsk\"", то обновление прошло успешно.




