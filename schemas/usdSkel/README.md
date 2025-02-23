# UsdSkel


## Questions

- Why do I need to have my skel:animationSource on my SkelRoot? Why can't it be on my geometry?
    - `prepend rel skel:animationSource = </World/SkelRoot/Animation>`
- How do I properly set up instancing prims with the same skeleton and different animations and positions?
- When might I want different bindTransforms & restTransforms?
- When might I want to use different skinning methods?
- Does it ever make sense for a mesh to have both joint based & blend shape animations at the same time? What does this look like?
- What are the tradeoffs from putting a skel animation on a skeleton instead of a skelRoot? Should I prefere to have my Skeleton apply the SkelBindingAPI or not?
