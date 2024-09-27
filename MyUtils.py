
def count_params(model):
  total_params = 0
  for param in model.parameters():
    num_elements = 1
    for dim in param.size():
        num_elements *= dim
    total_params += num_elements
  print(f"{total_params / 1000000:.1f} million parameters")
     

def visualize_detections(img, dets, labels=None, thresh=0.5, caption=None):
  # dets array format: [x1, y1, x2, y2, score]
  """Draw detected bounding boxes."""
  inds = np.where(dets[:, -1] >= thresh)[0]
  if len(inds) == 0:
      return

  # Find the index of the item with max confidence score
  top_idx = dets[:, -1].argmax()

  _, ax = plt.subplots(figsize=(12, 12))
  ax.imshow(img, aspect='equal')
  for i in inds:
      bbox = dets[i, :4] # Get the 1st 4 columns from the ith row
      score = dets[i, -1]
      label = labels[i] if labels is not None else None

      ax.add_patch(
          plt.Rectangle((bbox[0], bbox[1]),
                        bbox[2] - bbox[0],
                        bbox[3] - bbox[1], fill=False,
                        edgecolor='red' if i == top_idx else 'green', linewidth=3.5)
          )
      if label is not None:
          ax.text(bbox[0], bbox[3] - 2,
                  label,
                  bbox=dict(facecolor='blue', alpha=0.5),
                  fontsize=8, color='white')
      ax.text(bbox[0], bbox[1] - 2,
              '{:.3f}'.format(score),
              bbox=dict(facecolor='blue', alpha=0.5),
              fontsize=14, color='white')
  # plt.axis('off')
  plt.tight_layout()
  plt.draw()
  if caption is not None:
      plt.title(caption, fontsize=20)
  plt.show()
     
