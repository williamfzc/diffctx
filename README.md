# diffctx = diff context

Auto code reviewer powered by GPT + LSIF. All in one GitHub Action.

## Showcase

With a simple setup in your GitHub Action:

```yaml
- name: diffctx
  uses: williamfzc/diffctx@v0.1.4
  with:
    lang: "golang"
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
```

Diffctx will automatically analyse the diff (**and the context of diff**) every new PullRequests in your repo, and leave comments for indicating which part you should care most:

<img width="628" alt="image" src="https://user-images.githubusercontent.com/13421694/232233602-f59f5d82-31dc-489b-8501-791faeff2db9.png">

Based on [LSIF](https://microsoft.github.io/language-server-protocol/overviews/lsif/overview/), diffctx will not only analyse the lines contained by the diff, but also the full scope of your repo, and understand it well.

So it can better evaluate your changes and give more accurate suggestions from a global perspective.

## Usage

diffctx can be directly used with GitHub Action.

### Add OpenAI Api Key

<img width="816" alt="image" src="https://user-images.githubusercontent.com/13421694/232230719-1d827367-d766-4cc7-95d0-e8a0c3adbea8.png">

### Add to GitHub Action

```yaml
name: Test PR

# triggered by pull_request
on: [push, pull_request]

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
        uses: williamfzc/diffctx@v0.1.4
        with:
          # currently we support: golang/java/python
          lang: "golang"
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
```

### Done!

You can create a new PullRequest for test.

## How it works

1. Scan the repo and understand it well
2. Extract the sub graph influenced by the diff
3. Generate a summary from sub graph
4. Send the summary to AI for evaluation
5. Create a comment

The 1-3 is finished by [srctx](https://github.com/williamfzc/srctx).

## Cost

Token is expensive. So we did not intend to let AI scan all the codes at the beginning, but advanced and standardized the calculation part through the parser.

Everything can be done in one request. Which takes ~10s.

## Contribution

Issues, PRs and suggestions are welcome.

- [diffctx](https://github.com/williamfzc/diffctx): for the whole workflow
- [srctx](https://github.com/williamfzc/srctx): the core analyzer

## Roadmap

- Stable prompt
- Send AI the necessary code to make better suggestions
- Better comment format
- Extract more meaningful columns (like function definition) from code