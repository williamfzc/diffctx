# diffctx = diff context

A GitHub action for automatically evaluating the function level impacts of Pull Requests.

## Showcase

With a simple setup in your GitHub Action:

```yaml
- name: diffctx
  uses: williamfzc/diffctx@v0.2.2
  with:
    lang: "golang"
```

Diffctx will automatically analyse the diff (**and the context of diff**) every new PullRequests in your repo, and leave
comments for indicating which part you should care most:

![](https://user-images.githubusercontent.com/13421694/236665125-4968558b-8601-43d0-9618-97e146f93749.svg)

And leave a comment for helping evaluations.

<img width="697" alt="image" src="https://user-images.githubusercontent.com/13421694/236666915-5d403e4a-9cc1-4364-afbe-363cf82e5e49.png">

Based on [LSIF](https://microsoft.github.io/language-server-protocol/overviews/lsif/overview/), diffctx will not only
analyse the lines contained by the diff, but also the full scope of your repo, and understand it well.

## Usage

diffctx can be directly used with GitHub Action.

### Add to GitHub Action

```yaml
name: Test PR

# triggered by pull_request
on: [ push, pull_request ]

# for creating comments
permissions:
  pull-requests: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 2

      # ...

      - name: diffctx
        uses: williamfzc/diffctx@v0.2.2
        with:
          # currently we support: golang/python
          lang: "golang"
```

### Done!

You can create a new PullRequest for test.

### Still have a problem?

A real example can be found in: https://github.com/williamfzc/srctx/tree/test_diffctx

## How it works

1. Scan the repo and understand it well
2. Extract the sub graph influenced by the diff
3. Generate a summary from sub graph
4. Create a comment

## Supported Languages

Thanks to tree-sitter and LSIF, diffctx can support nearly all the popular languages.

| Languages | Status  |
|-----------|---------|
| Golang    | Done    |
| Python    | Done    |
| Java      | Working |

## Contribution

Issues, PRs and suggestions are welcome.

- [diffctx](https://github.com/williamfzc/diffctx): for the whole workflow
- [srctx](https://github.com/williamfzc/srctx): the core analyzer

## Roadmap

- More languages
- Better comment format
- Extract more meaningful columns (like function definition) from code
- Display graph in comment also
