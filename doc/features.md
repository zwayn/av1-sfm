# **Features**

## Context

Documentation used to describe with a bit more of details about the functions implemented in `src/modules/features.py`.
It is a work in progress and will be updated as we add more features.

## **_av1_match**

### Description

Do the matching between the current frame and its references.

The matching is done by using the motion vectors and the reference frame.
The motion vectors are pointing towards a reference frame. AV1 uses a 
buffer of 7 frames that can be used as a reference frame for a block.

Moreover based on how the motion vectors are computed during the encoding
process, we can interpolate the motion vectors to get matches with in-between
frames.

This function retrieves the matches using the motion vectors and the reference
and compute the interpolated matches.

#### Arguments

- `coord_block`: The list of the center coordinates of the blocks.  
- `motion_vectors`: The motion vectors.
- `reference_frame`: The reference frame.
- `matches`: Pandas dataframe to store the matches.
- `frame_number`: The current frame number.

#### Returns

- `matches`: The updated matches.


### Details

In our implementation, we replace traditional features with blocks out of the encoder. SIFT feature has 4 components:

1. x coordinate of the keypoint
2. y coordinate of the keypoint
3. scale
4. orientation

Instead of a keypoint, we use the center or the block. Therefore our new feature has 4 new components:

1. x coordinate of the center of the block
2. y coordinate of the center of the block
3. minimal size of the block (minimum between width and height)
4. orientation of the block (in radian. We compute the orientation of the gradient of the block)

*for more details regarding AV1 features, please refer to the [json_processing](json_processing.md) documentation*

When encoding a video, the encoder generates motion vectors for most of the blocks. Those motion vectors tell us how the block has moved between the current frame and the reference frame. In a way it performs block matching between our frame and the reference frame.

AV1 uses a buffer of 7 frames that can be used as a reference frame for a block. The encoder tends to get the farest reference frame possible for the motion vector, performing interpolation and extrapolation when computing the motion vector.

*For more details about the temporal motion vector computation, please refer to the paper [A Technical Overview of AV1](https://arxiv.org/abs/2008.06091)*
