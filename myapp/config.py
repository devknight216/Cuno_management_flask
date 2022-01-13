# For anything that doesn't change between production and development
class Config(dict):
    pass

class ProductionConfig(Config):
    DEBUG = False
    # Use minified versions for faster loads
    BOOTSTRAP_JS = "/static/js/boostrap.bundle.min.js"
    BOOTSTRAP_CSS = "/static/css/bootstrap.min.css"

class DebugConfig(Config):
    DEBUG = True
    # Don't use minified versions 
    BOOTSTRAP_JS = "/static/js/bootstrap.bundle.js"
    BOOTSTRAP_CSS = "/static/css/bootstrap.css"