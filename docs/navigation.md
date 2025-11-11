# Navigation

The structure of this software package is described on the ["Software design"](software-design.md) page, which is also accessible via the sidebar.

Installation notes are available on the ["How to install"](how-to-install.md) page.
Notes on running simulations are available on the corresponding ["How to run"](how-to-run.md) page. 

Links to test scripts are provided under [`Tests`](tests-reference.md).
Look under under "Simulation tools" in the sidebar for more complete examples and further information.

The key driver of a simulation is the [`Info.json`](simulation-tools/info-reference.md) file: care must be taken to match the "job name" implied by this file (a string constructed from the model coefficients and parameters specified by it) with its parent folder name, such that output files are placed correctly.

Refer to the links under "Python modules" to see documentation of the 
[`langevin` Python package](https://pypi.org/project/langevin/). The underlying `C++` core is documented under ["C++ source"](cplusplus-source/index.md) using `Doxygen`.

<!-- //// note | Some title
/// details | Summary
    type: warning
content
///
Content
//// -->
<!-- 
/// details | Warning
    type: warning

Describe the warning
/// -->

<!-- ??? optional-class "Summary"
    Here's some content.

??? success
   Content.

??? warning classes
   Content.

???+ note "Open styled details" -->


<!-- text^a\ superscript^ -->

<!-- First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell


Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus. -->
<!-- 
> ```
  a fenced block

> with blank lines
  ``` -->


<!-- -   [X] item 1
    *   [X] item A
    *   [ ] item B
        more text
        +   [x] item a
        +   [ ] item b
        +   [x] item c
    *   [X] item C
-   [ ] item 2
-   [ ] item 3 -->


--> =/= <--

CH~3~CH~2~OH

text~a\ subscript~