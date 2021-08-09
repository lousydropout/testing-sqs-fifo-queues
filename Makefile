build-WriteToDDBLambda:
	cp handler.py ${ARTIFACTS_DIR}/

build-SendMessagesToFIFOQueueLambda:
	cp send_messages.py ${ARTIFACTS_DIR}/

build-SendMessagesToStdQueueLambda:
	cp send_messages.py ${ARTIFACTS_DIR}/
