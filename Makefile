build-WriteToDDBLambda:
	cp handler.py ${ARTIFACTS_DIR}/

build-SendMessagesToFIFOQueue:
	cp send_messages.py ${ARTIFACTS_DIR}/

build-SendMessagesToStdQueue:
	cp send_messages.py ${ARTIFACTS_DIR}/
