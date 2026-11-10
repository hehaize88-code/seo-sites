import {embed} from './embedding.mjs';import sharp from 'sharp';
console.log('Loading local image model...');console.log('Dimensions:',(await embed(await sharp({create:{width:224,height:224,channels:3,background:'#ffffff'}}).png().toBuffer())).length);
