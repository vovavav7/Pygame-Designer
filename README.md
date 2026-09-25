# PygameDesigner

A visual UI designer and runtime library for Pygame applications.

## Description

PygameDesigner is an open-source tool that allows you to visually create user interfaces for Pygame applications.

The package contains both a visual designer and a Python library for loading and displaying interfaces created with the designer.

After installing the package, the visual designer can be launched directly from the terminal:

```bash
PygameDesigner
```

Designed interfaces can be saved as JSON files and loaded into a Pygame application using Python.

## Getting Started

### Dependencies

* Python 3.10 or newer
* Pygame

PygameDesigner is installed using `pip`.

### Installing

Install PygameDesigner from PyPI:

```bash
pip install PygameDesigner
```

If Pygame is not already installed:

```bash
pip install pygame
```

### Executing program

After installation, start the visual designer from any terminal:

```bash
PygameDesigner
```

To use a design in your own Pygame project:

1. Create your interface using the PygameDesigner visual editor.
2. Save the interface as a JSON file.
3. Put the JSON file in your Pygame project.
4. Import PygameDesigner in your Python program.
5. Load the JSON file using `PygameDesigner.load()`.
6. Draw the interface using `PygameDesigner.draw()`.

Example:

```python
import pygame
import PygameDesigner

pygame.init()

ui = PygameDesigner.load("test_ui.json")

win = ui.window_settings
screen = pygame.display.set_mode(
    (win["width"], win["height"])
)

pygame.display.set_caption(win["title"])


def my_button_action():
    print("Button clicked!")


ui.get("click_me_btn").on_click = my_button_action


running = True
clock = pygame.time.Clock()

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    PygameDesigner.draw(ui, events, screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

## Help

If `PygameDesigner` is not recognized as a command, make sure the package is installed correctly:

```bash
pip install --upgrade PygameDesigner
```

You can check whether the package is installed with:

```bash
pip show PygameDesigner
```

If the command is still not available, make sure Python's `Scripts` directory is included in your system `PATH`.

For other problems, open an issue in the GitHub repository.

## Authors

Volodymyr

GitHub: [@jedik07](https://github.com/jedik07)

## Version History

* 0.1

  * Initial release
  * Visual UI designer
  * JSON-based UI files
  * Pygame integration
  * Button click events
  * Python API for loading and drawing interfaces

## License

This project is licensed under the GNU General Public License v3.0.

See the [LICENSE](LICENSE) file for the full license text.

## Acknowledgments

* [Pygame](https://www.pygame.org/) - Pygame framework
* [Python](https://www.python.org/) - Programming language
* [PyPI](https://pypi.org/) - Package distribution
