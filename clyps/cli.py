from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import click
from clyps.kb import KnowledgeBase
from clyps.fact import Fact
from clyps.rule import Rule


@click.command()
def cli():
    """REPL interface for CLYPS with CLIPS-like syntax."""
    kb = KnowledgeBase()
    history = InMemoryHistory()
    click.echo("CLYPS REPL with CLIPS-like syntax. Type (exit) or (quit) to leave.")
    while True:
        try:
            # Prompt the user for input using prompt_toolkit
            command = prompt("? ", history=history)

            # Exit the REPL
            if command in ["(exit)", "(quit)"]:
                break

            # Add a fact
            elif command.startswith("(assert"):
                fact_str = command[len("(assert ") : -1].strip()
                fact = Fact.from_string(fact_str)
                kb.add_fact(fact)
                click.echo(f"=> Fact asserted: {fact}")

            # Add a rule
            elif command.startswith("(defrule"):
                rule = Rule.from_string(command)
                kb.add_rule(rule)
                click.echo(f"=> Rule defined: {rule}")

            # Perform inference
            elif command == "(run)":
                kb.infer()
                click.echo("=> Inference completed.")
                click.echo("Current facts:")
                for fact in kb.facts:
                    click.echo(fact)

            # Unknown command
            else:
                click.echo(
                    "Unknown command. Use (assert <fact>), (defrule <name> <rule>), (run), (exit) or (quit)."
                )

        except Exception as e:
            click.echo(f"Error: {e}")


if __name__ == "__main__":
    cli()
