#!/usr/bin/env python
"""
ملف التشغيل الإنتاجي للنظام
"""

import os
import sys
from pathlib import Path

# إضافة المسار
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

def start_production():
    """بدء التشغيل في بيئة الإنتاج"""
    
    # 1. تحميل المتغيرات البيئية
    from dotenv import load_dotenv
    load_dotenv()
    
    # 2. ضبط إعدادات Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')
    
    # 3. استيراد وتشغيل تطبيق WSGI
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    
    # 4. عرض معلومات النظام
    print("\n" + "="*60)
    print("🚀 نظام إدارة الأدوية - الإنتاج")
    print("="*60)
    
    from django.conf import settings
    print(f"🔧 الوضع: {'Production' if not settings.DEBUG else 'Development'}")
    print(f"🗄️ قاعدة البيانات: {settings.DATABASES['default']['ENGINE']}")
    print(f"🌐 الإصدار: {settings.VERSION if hasattr(settings, 'VERSION') else '1.0.0'}")
    print("="*60 + "\n")
    
    return application

def start_development():
    """بدء التشغيل في بيئة التطوير"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')
    
    import django
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    # تشغيل سيرفر التطوير
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

if __name__ == '__main__':
    # التحقق من بيئة التشغيل
    env = os.getenv('DJANGO_ENV', 'development')
    
    if env == 'production':
        # استخدام Gunicorn في الإنتاج
        try:
            import gunicorn.app.base
            from gunicorn.six import iteritems
            
            class GunicornApp(gunicorn.app.base.BaseApplication):
                def __init__(self, app, options=None):
                    self.options = options or {}
                    self.application = app
                    super().__init__()
                
                def load_config(self):
                    config = dict([(key, value) for key, value in iteritems(self.options)
                                   if key in self.cfg.settings and value is not None])
                    for key, value in iteritems(config):
                        self.cfg.set(key.lower(), value)
                
                def load(self):
                    return self.application
            
            # إعدادات Gunicorn
            options = {
                'bind': '0.0.0.0:' + os.getenv('PORT', '8000'),
                'workers': 4,
                'worker_class': 'sync',
                'timeout': 120,
                'accesslog': '-',
                'errorlog': '-',
                'loglevel': 'info'
            }
            
            app = start_production()
            GunicornApp(app, options).run()
            
        except ImportError:
            print("⚠️ Gunicorn غير مثبت. جاري استخدام سيرفر التطوير...")
            start_development()
    
    else:
        # بيئة التطوير
        print("🔧 الوضع: تطوير")
        start_development()