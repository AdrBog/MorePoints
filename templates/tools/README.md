Here you can add your own tools to edit files

At the moment there is only the text editor, but if you want to replace the current text editor with your own text editor, you should save it here.

After adding the file here, you have to edit the path to the template in **utils/tools.py**

If you want to create your own tool for other types of files, you should also add it here

Then create the flask path in **utils/tools.py**

Finally, set More Points to open these types of files with the tool that is done in **config/config.json**

```json
{
    "extensions": ["foo", "bar"],
    "tool": "test_tool"
}
```
