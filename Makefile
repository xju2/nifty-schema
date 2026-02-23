PROTOBUF_VERSION = 3.33.5
PROTOC_ZIP = protoc-$(PROTOBUF_VERSION)-linux-x86_64.zip
INSTALL_DIR = $(HOME)/.local
BIN_DIR = $(INSTALL_DIR)/bin

.PHONY: install-protoc clean-protoc
install-protoc:
	@echo "Checking for unzip..."
	@which unzip > /dev/null || (echo "Error: unzip is not installed. Run 'sudo apt install unzip'" && exit 1)

	@echo "Downloading protoc v$(PROTOBUF_VERSION)..."
	curl -LO https://github.com/protocolbuffers/protobuf/releases/download/v$(PROTOBUF_VERSION)/$(PROTOC_ZIP)

	@echo "Unzipping to $(INSTALL_DIR)..."
	mkdir -p $(INSTALL_DIR)
	unzip -o $(PROTOC_ZIP) -d $(INSTALL_DIR) bin/protoc 'include/*'

	@echo "Cleaning up zip file..."
	rm $(PROTOC_ZIP)

	@echo "------------------------------------------------------"
	@echo "Installation complete!"
	@echo "Ensure $(BIN_DIR) is in your PATH."
	@echo "Run: export PATH=\$${PATH}:$(BIN_DIR)"
	@echo "------------------------------------------------------"

clean-protoc:
	rm -f $(BIN_DIR)/protoc
	rm -rf $(INSTALL_DIR)/include/google/protobuf


.PHONY: build_cpp
build_cpp:
	cmake -B build -S .
	cmake --build build --config Release

.PHONY: install
install:
	uv pip install -e .

.PHONY: tests
tests:
	uv run pytest
