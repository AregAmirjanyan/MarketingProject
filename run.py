import uvicorn
from payment_optimizer.api.endpoints import app

""" if __name__ == '__main__':
    uvicorn.run("payment_optimizer.api.endpoints:app", reload=True) 
 """

if __name__ == '__main__':
    uvicorn.run(app) 