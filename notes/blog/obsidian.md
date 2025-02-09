title: Two years with Obsidian: How notes changed the way I store information
description: Quick intro on the note-taking app Obsidian, how I use it, and my takeaways.
tags: productivity
tags: obsidian
published: 2025-02-09
modified: 2025-02-09
template: blog
length: 7
---

I've been storing and keeping track of information in various ways for a long time. First using physical notes, then simple digital text files, and finally I jumped from app to app as I encountered issues that irritated me that I had no control over.

Near the tail end of 2022, I came across what I thought might be the answer to all my woes: a note-taking app built by a small team, with the name of [Obsidian](https://obsidian.md/){:target="_blank"}.

## What's in an Obsidian?

Obsidian is a multi-platform note-taking and writing app. Simple enough. But aren't there plenty of those around? Yes absolutely, but they each have downsides that I wasn't able to settle with long-term. With [Google Cloud](https://docs.google.com/){:target="_blank"} it was the difficult of linking between notes (this has improved since but it's still not quite what I want). With [Evernote](https://evernote.com/){:target="_blank"} my notes were in a proprietary format and stuck in the cloud. [Notion](https://www.notion.com/){:target="_blank"} also had the cloud-first problem and stored in an awkward non-standard Markdown format. And the list goes on.

Here's what Obsidian provides that sold it to me:

- **Local-first** providing tangible `.md` files in a local directory structure I can interact with.
- **Portable notes** in standard Markdown format allowing me to easily migrate to other platforms.
- **Links between notes** gives the ability to quickly move to related notes using wiki-style links.
- **YAML frontmatter** rendering key-value pairs of metadata for each note in a beautiful way.
- **Graphs and canvases** allowing me to easily visualize notes and their connections.
- **Mobile friendly** with support for all of the same features that the desktop version offers.
- **Native sync** providing [end-to-end encrypted sync and version control](https://obsidian.md/sync){:target="_blank"} for a modest monthly fee.
- **Extensible** with a broad catalog of [community-created plugins](https://obsidian.md/plugins){:target="_blank"} and themes.

![Screenshot of my Obsidian vault opened on the graph view](/static/images/obsidian/obsidian.png)
<span class="img-caption">Screenshot of my Obsidian vault opened on the graph view.</span>

## Why store information?

The way people interact with pieces of information is very personal and differ from person to person, but these are the main reasons I've been maintaining a repository of notes over the past decade or so:

- Noting down information that I know I don't need in the short-term **frees cognitive space** to think about and remember other things.
- Counter-intuitively, noting down information that I _do_ need in the short-term **helps me remember** them better. The simple act of writing down reminders engraves them in my short-term memory.
- Doing research in notes **prevents me from doing duplicative research** the next year or the next decade. At the very least, it gives me a foundation to work with instead of starting from scratch multiple times.
- It's a sort of **knowledge insurance for the future**. I intend to live for at least a handful more decades, and that's plenty of time to forget things (either because of an illness, or simply because it's been so long).
- If I were to **author an auto-biography** in my later years, all of the material would already be there, waiting to be pieced together in a coherent story.

So with that said, what are the kinds of notes that I have in Obsidian? Glad you asked! Here's a non-exhaustive list (in no particular order) of different note categories, with some examples for each:

- **Journaling & retrospectives** ("Year 2024", "2025-02-09", ...)
- **Brainstorming** ("3D printing ideas", "Photography ideas", ...)
- **Knowledge** ("Interesting urbanism studies", "How to count things in Japanese", ...)
- **Personal** ("5 years life plan & goals", "History of addresses lived at", ...)
- **Career** ("Onboarding to a new job", "Employment history", ...)
- **Finances** ("Tax return forms to expect", "TFSA contribution table", ...)
- **Health** ("Eye exam & prescription history", "Family health history", ...)
- **Trips & events** ("Pre-travel checklist", "List of flights taken", ...)
- **Media consumed & backlog** ("Books I've read", "Christmas films I want to watch", ...)

![Screenshot of a note I created to act as an overview of my personal notes](/static/images/obsidian/olivier.png)
<span class="img-caption">A note I created to act as an overview of notes about me.</span>

## Templates to reduce repetition

The first community-built plugin that I ended up trying out was [QuickAdd](https://obsidian.md/plugins?id=quickadd){:target="_blank"}. This plugin allows you to create custom commands in the command palette configured to duplicate a specific template note. This means that you could create for example a note called "New trip template" and configure a command called "Add new trip" which would duplicate that particular note and open it for you to fill out as desired.

In my Obsidian vault I've set-up many of these templates which both saves me a lot of time, and ensures consistency between notes of the same category / type. When I open the command palette and search for "QuickAdd", they all show up:

![Screenshot of the command palette showing QuickAdd](/static/images/obsidian/quickadd.png)
<span class="img-caption">A few of the QuickAdd commands I have set-up.</span>

Let's say I'm going on a trip soon. I select the **Add new trip** command, enter a name ("Trip to the Land of OOO") and a note is automatically created, stored at the expected location, with the relevant template (both the YAML metadata and the Markdown note itself) ready for me to fill out!

![Screenshot of a generated trip built from its template](/static/images/obsidian/new-trip.png)
<span class="img-caption">Looking forward to my upcoming trip to OOO!</span>

Since templates mean I get to create a lot of notes really easily, I wanted to prevent an potential issue where my directories would be full of notes of all kinds mixed together. To solve this, I have the templating plugin set-up to place the notes in a relevant `_items/` directory within the root-level category directory. This allows me to easily find the non-templated notes (in this case, something like "Packing list").

![Screenshot of the directory structure of my vault, showing the Trips notes](/static/images/obsidian/trips-dirs.png)
<span class="img-caption">The directory structure of my vault, showing the Trips notes.</span>

## Scripting to leverage external metadata

One of the advantages of using a local-first notes app with an open portable format is that I can easily interact with the notes outside of the note taking app itself. This means that I can, among other things, build custom scripts or pipelines that can create or modify notes.

I currently do this for three types of notes:

- Batch-converting Google Contacts metadata to _people notes_.
- Generating _concert notes_ from a [setlist.fm](https://www.setlist.fm/){:target="_blank"} URL which then auto-fills metadata like venue, tour name, and setlist.
- Injecting metadata into _media notes_ using public APIs like [IGDB](https://www.igdb.com/api){:target="_blank"} to auto-fill metadata like release date, synopsis, rating, and more.

![Screenshot of the Back to the Future note after injecting IMDb metadata](/static/images/obsidian/back-to-the-future.png)
<span class="img-caption">The Back to the Future note after injecting IMDb metadata.</span>

## Querying notes to render tables

Something that I missed after having used Notion for a few years was the ability to create rendered tables out of notes with custom columns, filters, and sorting. Obsidian doesn't have that built-in (though it is [on the roadmap](https://obsidian.md/roadmap/){:target="_blank"}), but there is a community-built plugin called [Dataview](https://obsidian.md/plugins?id=dataview){:target="_blank"} that offers most of what I was looking for.

Dataview works by parsing code blocks starting with ````dataview` containing what they call Dataview Query Language (it's essentially SQL) and renders them based on that query. The query contains statements allowing you to do parsing, filtering, sorting, and grouping. It even has some limited support for expressions and function-calling.

I currently use Dataview for rendering tables of my media backlog, trips, and events.

Below you'll find an example of a Dataview table note I created and how it renders. The query essentially translates to: build a table with three columns (title, year, rating) made up of all notes of category "films" (excluding the template note), and sort by [IMDb](https://www.imdb.com/){:target="_blank"} rating.

```
table without id
	string("[[" + file.path + "|" + title + "]]") as Title,
	year as Released,
	apiRating as "IMDb"
where
	contains(category,[[Films]]) and
	!contains(file.name,"template")
sort apirating desc
```

![Screenshot of the "Films by IMDb ratings" table](/static/images/obsidian/films-table.png)
<span class="img-caption">The rendered table for films* sorted by IMDb user ratings.</span>

<span class="text-small">*Yes I know, I need to get to Coppola's The Godfather trilogy sometime.</span>

## Journaling to clear my mind

I have a confession to make. Before 2024 I'd never try journaling. I decided to give it a try early last year and it's been useful so far! It helps me remember what I do on a day-to-day basis, track illnesses like the flu, and put nagging thoughts in order. On that first point, it's already helping me quickly answer questions like "when was the last time I chatted with so-and-so, and what did we talk about?" (the search and the backlink functionalities of Obsidian doing the heavy-lifting).

Since I was planning to do journaling every day, I wanted to make the process as streamlined and easy as possible for me, as to remove any cognitive friction that would push me towards skipping a day (or ten). This is the workflow I ended up building:

- A template for the daily notes (`_meta/templates/Daily template`).
- The built-in [Daily notes plugin](https://help.obsidian.md/Plugins/Daily+notes){:target="_blank"} to manage and format daily notes (`YYYY/MM-MMMM/YYYY-MM-DD-dddd`)
- The [Calendar plugin](https://obsidian.md/plugins?id=calendar){:target="_blank"} to add a calendar in the sidebar that links to the relevant daily notes.

![Screenshot of the Calendar plugin](/static/images/obsidian/calendar.png)
<span class="img-caption">Screenshot of the Calendar plugin.</span>

![Screenshot of the template I use for daily journaling](/static/images/obsidian/daily-template.png)
<span class="img-caption">The template I use for daily journaling.</span>

## Takeaways

And now, two years with Obsidian, here are my takeaways:

- The effort of migrating to yet another app was daunting, but now that all my notes are in an open format, I'm much less concerned about any hypothetical migration in the future (if this app were to cease development, for example).
- It's not necessary to come up with all the notes you'll ever need right away. Managing personal notes is a marathon, not a sprint. In fact, it's better to wait until the time that you need a particular note created to create it (instead of trying to proactively come up with future use-cases that haven't come to pass yet).
- Reinventing the wheel is not always the best use of time. It's worth looking if someone else built a similar pipeline, plugin, or system that gets you closer to what you want to achieve.
- Keeping up with challenges (like journaling) is much easier if you reduce the friction necessary to complete these challenges. Make it so easy that skipping a day would sound silly.

I even have a small backlog of improvement ideas for the future:

- Play around with different themes and styles (I'm still using the default theme).
- Build a sort of "CRM" (using that term very loosely) to help me maintain relationships better.
- Look into plugins to do task management and habit tracking.
- Build a small script that could pull weather data into my daily notes.
- Write periodic year and quarter retrospective notes (highlights, trips taken, people hung out with, etc.)

If you use Obsidian, or if you are thinking of giving it a try, I would love to hear how you approach note-taking!
