class Config:
    SECRET_KEY = 'super_secret_key'
    MONGO_URI = "mongodb+srv://sasekaninkuri560:eeszAgqQPJu4umai@cluster0.ktevnlj.mongodb.net/securedlink"
    SESSION_TYPE = 'filesystem'  # valid options: 'filesystem', 'redis', 'mongodb', etc.
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True