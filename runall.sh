export PYTHONPATH=/media/mohayemin/Work/PhD/soar-fork

# for file in conv_for_text alexnet densenet_conv_block densenet_trans_block gan_generator lenet two_conv vgg19 densenet_part1 embed_conv1d_linear img_autoencoder three_linear vgg11 word_autoencoder conv_pool_softmax densenet_part2 gan_discriminator img_classifier tutorial vgg16; do
for file in densenet_conv_block densenet_trans_block gan_generator lenet two_conv vgg19 densenet_part1 embed_conv1d_linear img_autoencoder three_linear vgg11 word_autoencoder conv_pool_softmax densenet_part2 gan_discriminator img_classifier tutorial vgg16; do
  echo $file
  python3 synthesis/synthesizer/tf_to_torch/torch_synthesizer.py -b $file -errmsg
done
