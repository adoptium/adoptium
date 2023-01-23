# The tweets/ folder

To create a new tweet create a new `*.tweet` file in this `tweets/` folder.

<kbd>[Create new tweet](../../../new/main/?filename=tweets/<your-path>.tweet)</kbd>

## Example

Create a new file `tweets/hello-world.tweet` with the content

> Hello, world!

You can use subfolders, e.g. `tweets/2019-02/hello-world.tweet`, as long as the file is in the `tweets/` folder and has the `.tweet` file extension

## Advanced example

See the [Twitter Together README](https://github.com/twitter-together/action#advanced-tweeting) to learn advanced use-cases.

## Notes

- Only newly created files are handled, deletions, updates or renames are ignored.
- `*.tweet` files will not be created for tweets you send out directly from twitter.com
- If you need to rename an existing tweet file, please do so locally using [`git mv old_filename new_filename`](https://help.github.com/en/articles/renaming-a-file-using-the-command-line), otherwise it may occur as deleted and added which would trigger a new tweet.
- your message must fit into a single tweet
