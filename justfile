set shell := ["bash", "-cu"]

update input:
	@rm next-step.md
	@echo "{{input}}" >> next-step.md

	cat next-step.md

nix-init:
    @echo "Starting nix-shell and sourcing venv"
    @nix-shell --command "source venv/bin/activate; return"
