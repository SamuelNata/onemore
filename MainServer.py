from serverSide.Server import RequestHandler, RequestReciver
from utils.Utils import logf

rr = RequestReciver()
rh = RequestHandler()

logf("Start Handler", True)
rh.start()
logf("Start Reciver", True)
rr.start()

rr.join()
rh.join()