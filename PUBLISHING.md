# Publish this result on GitHub

Use this directory as a fresh publication folder. Keep it separate from the
optimization project's working directory. You do not need to start another
Codex search or validation session to publish the checked certificate.

## Upload using your browser

1. Download `n68-publication-kit.zip` and extract it. Inside is a folder named
   `n68-publication-kit`. Its contents are the repository files.
2. If desired, edit the attribution sentence in `README.md` to include your
   preferred public name. README and this publishing guide are not covered by
   the geometry/code hash manifest, so this edit does not invalidate it.
3. Sign in to GitHub and open <https://github.com/new>.
4. Select your own account as Owner. Enter repository name
   `certified-square-packing-68`, choose **Public**, and use description
   `Exact certificate for 68 unit squares in side 8.798795237221.`
5. Turn on **Add a README file** so GitHub creates an initial main branch. Click
   **Create repository**. You will replace the initial README in the next step.
6. On the repository's **Code** page, select **Add file → Upload files**. Open
   your extracted folder and drag its contents into the upload area. Upload the
   individual files at the repository root; do not upload only the ZIP or put
   another `n68-publication-kit` directory around them. GitHub's web uploader
   accepts up to 100 files at a time, each at most 25 MiB; this kit is below
   both limits.
7. Enter commit message `Publish exact n=68 certificate and verification`.
   Select **Commit directly to the main branch** and confirm **Commit changes**.
   If your account's rules require a new branch, use that branch and merge its
   pull request instead.
8. Confirm that the main repository page shows the detailed README and diagram.
   Open `n68.json` and check its `n` is 68 and `container_side` is
   `8798795237221/1000000000000`.

## Make a tagged release

9. On the repository page, click **Releases**, then **Create a new release** or
   **Draft a new release**.
10. Choose a new tag `v1.0.0`, with target branch `main`. Use title
    `Certified n=68 packing: side 8.798795237221`.
11. In the description, describe the exact side, both verification commands,
    the refinement of Jake Loyd's construction, and unresolved record priority.
    The repository README already contains these details.
12. Attach your unchanged `independent-audit.zip` as supporting material. Its
    SHA-256 should be
    `4edf42a7ad5f1f17363fc728c6e08cd7614d4cc1dd74b6515bf5c25b7d07215b`.
    The original small publication-kit ZIP is optional as another asset. If you
    edited its README after extraction, GitHub's automatically generated source
    ZIP will reflect that edit, while the original kit ZIP will not.
13. Review the release and click **Publish release**. Save the release URL and
    full commit hash. Keep the first release's certificate available unchanged;
    publish later improvements under a new version/tag.

## Submit for table review

14. Open <https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues>.
    Create an issue proposing the certified n=68 bound. Include your release
    URL, exact side, certificate hash, verification commands, Jake Loyd
    attribution, and comparison with franciscouzo's posted file. Ask whether the
    earlier n=68 submission affects priority and what attribution the maintainer
    prefers for a refinement.
15. Share the release link on social media using the precise description
    “certified refinement / proposed record,” with the side and reproducible
    files. Update the status when the table maintainer responds.

GitHub publication records public disclosure of these files. Mathematical
priority and table credit depend on comparison and review; a private discovery
date in supplied metadata does not settle either.

## Official GitHub instructions

- <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository>
- <https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository>
- <https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository>
