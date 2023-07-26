# diffctx = diff context

[![Latest Release](https://img.shields.io/github/v/release/williamfzc/diffctx?include_prereleases)](https://github.com/williamfzc/diffctx/releases/latest)

A GitHub action for automatically evaluating the logic level impacts of Pull Requests.

## Showcase

With a simple setup in your GitHub Action:

```yaml
- name: diffctx
  uses: williamfzc/diffctx@v0.3.10
  with:
    lang: "golang"
```

Diffctx will automatically analyse the diff (**and the context of diff**) every new PullRequests in your repo, and leave
comments for indicating which part you should care most:

![](https://user-images.githubusercontent.com/13421694/236665125-4968558b-8601-43d0-9618-97e146f93749.svg)

And leave a comment for helping evaluations.

<img width="912" alt="image" src="https://github.com/williamfzc/srctx/assets/13421694/46de1eaa-efd2-496e-ba85-838e3da1063c">

> https://github.com/williamfzc/srctx/pull/52

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
        uses: williamfzc/diffctx@v0.3.10
        with:
          # see the `Supported Langs` for details
          lang: "golang"
```

### Done!

You can create a new PullRequest for test.

## Supported Languages

### Overview

| Language | Ready? | Keyword in yaml | Real-world Sample                                                                                                 |
|----------|--------|-----------------|-------------------------------------------------------------------------------------------------------------------|
| Golang   | ✅      | `golang`        | [ci.yml](https://github.com/williamfzc/srctx/blob/test_diffctx/.github/workflows/ci.yml)                          |
| Java     | ✅      | `java`          | [main.yml](https://github.com/williamfzc/java-diffctx-sample/blob/main/.github/workflows/main.yml)                |
| Kotlin   | ✅🚧    | `kotlin`        | [build.yml](https://github.com/williamfzc/kt-diffctx-sample/blob/main/.github/workflows/build.yml)                |
| NodeJs   | ✅      | `node`          | [build.yml](https://github.com/williamfzc/node-diffctx-sample/blob/master/.github/workflows/grpc-tools-build.yml) |
| Python   | ✅      | `python`        | [run-test.yml](https://github.com/williamfzc/py-diffctx-sample/blob/main/.github/workflows/run-tests.yml)         |

### Want more langs?

Thanks to tree-sitter and LSIF, diffctx can support nearly all the popular languages.

https://lsif.dev/

Adding a new language support is not hard. PullRequests are always welcome!

## How it works

1. Scan the repo and understand it well
2. Extract the sub graph influenced by the diff
3. Generate a summary from sub graph
4. Create a comment

## Contribution

Issues, PRs and suggestions are always welcome.

- [diffctx](https://github.com/williamfzc/diffctx): for the whole workflow
- [srctx](https://github.com/williamfzc/srctx): the core analyzer

## Roadmap

- [ ] More languages
- [ ] Better comment format
- [ ] Extract more meaningful columns (like function definition) from code
- [ ] Display graph in comment also
