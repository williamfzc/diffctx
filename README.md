# diffctx = diff context

A GitHub action for automatically evaluating the logic level impacts of Pull Requests.

## Showcase

With a simple setup in your GitHub Action:

```yaml
- name: diffctx
  uses: williamfzc/diffctx@v0.2.3
  with:
    lang: "golang"
```

Diffctx will automatically analyse the diff (**and the context of diff**) every new PullRequests in your repo, and leave
comments for indicating which part you should care most:

![](https://user-images.githubusercontent.com/13421694/236665125-4968558b-8601-43d0-9618-97e146f93749.svg)

And leave a comment for helping evaluations.

<img width="952" alt="image" src="https://github.com/williamfzc/diffctx/assets/13421694/63739d01-b7dc-4947-8e3d-2e6c5ed0530c">

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
          # at least
          fetch-depth: 2

      # ...

      - name: diffctx
        uses: williamfzc/diffctx@v0.3.1
        with:
          # currently we officially support: 
          # - golang
          # - python
          # - java
          # - kotlin
          # - node
          lang: "golang"
```

### Done!

You can create a new PullRequest for test.

### Still have a problem?

A real example can be found in: https://github.com/williamfzc/srctx/pull/49

## How it works

1. Scan the repo and understand it well
2. Extract the sub graph influenced by the diff
3. Generate a summary from sub graph
4. Create a comment

## Supported Languages

Thanks to tree-sitter and LSIF, diffctx can support nearly all the popular languages.

https://lsif.dev/

## Contribution

Issues, PRs and suggestions are always welcome.

- [diffctx](https://github.com/williamfzc/diffctx): for the whole workflow
- [srctx](https://github.com/williamfzc/srctx): the core analyzer

## Roadmap

- [ ] More languages
- [ ] Better comment format
- [ ] Extract more meaningful columns (like function definition) from code
- [ ] Display graph in comment also
