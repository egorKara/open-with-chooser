# 🔐 Настройка аутентификации GitHub

## ⚠️ Проблема
GitHub больше не поддерживает аутентификацию по паролю для Git операций.

## 🎯 Решение: 2 варианта

### 🔑 Вариант 1: SSH ключ (рекомендуется)

#### Шаг 1: Добавьте SSH ключ на GitHub
1. **Скопируйте ключ** (уже готов):
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC/rGzeNmzRdC9uEV+yA+/CVstMZJzJgFaIBbKpsmi+I+7U4OgBqyVUme2xccx05BhYrmasAbDJJWpcjmwv6LDpieCz/YjBL01zsEOalY2j2anSCP2daPJPl/BxCy8QxLd153Eb+JZ3OF3g+yGcMRRhmgQ9vUDZxHQqYfgwCVNIYbqWDhCcCVDW4Ha4kYzvMNgNg4Q2jx7wbxyyb7enwk3t6LOYVjxsh9WFPSEma4a+vUXLUjQX6uyJlaYfBS6UyVdKSq+ZsSZk+J6AYp7Q9oeN7xWNpZWixteEPIsUVJX7OF8qpRGLMZaVtf863IkYBSg4rYB5cMsk4QgeJcLmgvwz+pcs9izk3tAvWX1xFJ7wwRr1QGue8Esnzxlw6b6asQyNcLxN6UL2ZouR4UF2dXdtLyyEvcFZ25kIGFzg4ZYLKZ+GiN//V0JimBZXmrNc0mtx8mGKfQxutKUEZlKeXY6KGXT6nr27vO9WDdNkTmnURT62YNATI3Bt9aACethM170= emergency-access
```

2. **Откройте**: https://github.com/settings/keys
3. **Нажмите**: "New SSH key"
4. **Заполните**:
   - Title: `Open With Chooser SSH Key`
   - Key: *вставьте скопированный ключ*
5. **Нажмите**: "Add SSH key"

#### Шаг 2: Проверьте соединение
```bash
ssh -T git@github.com
# Должно быть: "Hi egorKara! You've successfully authenticated..."
```

#### Шаг 3: Опубликуйте репозиторий
```bash
git push -u origin main
```

---

### 🎟️ Вариант 2: Personal Access Token

#### Шаг 1: Создайте токен
1. **Откройте**: https://github.com/settings/tokens
2. **Нажмите**: "Generate new token (classic)"
3. **Заполните**:
   - Note: `Open With Chooser`
   - Expiration: `90 days` (или больше)
   - Scopes: ✅ `repo`
4. **Нажмите**: "Generate token"
5. **Скопируйте токен** (показывается один раз!)

#### Шаг 2: Настройте HTTPS
```bash
git remote set-url origin https://github.com/egorKara/open-with-chooser.git
```

#### Шаг 3: Опубликуйте репозиторий
```bash
git push -u origin main
# Username: egorKara
# Password: ВАШ_ПЕРСОНАЛЬНЫЙ_ТОКЕН
```

---

## ✅ После успешной публикации

Создайте первый релиз:
1. **Перейдите**: https://github.com/egorKara/open-with-chooser/releases
2. **Нажмите**: "Create a new release"
3. **Заполните**:
   - Tag: `v2.0.1`
   - Title: `🎉 Open With Chooser Enhanced v2.0.1`
   - Description: Скопируйте из README.md
4. **Прикрепите**: `scripts/open-with-chooser-installer.sh`
5. **Publish release**

🎉 **Готово! Репозиторий опубликован!**
