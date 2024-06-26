#! /bin/zsh

# script for checking Ralph Lauren images
# version: 1.4.4
# include session name in the report
# created by Zeric Chan
#
# plan
# 1) [done] check image spec
# 2) [done] check filename with 1 character difference and rename them
# 3) [done] consider insert
# 4) [working] better report, include info about oldname + newname
# 
# issues
# 1) renameing images with 1 missing character, only the first alphabet will be removed if there are more than 1 of the same alphabet
# 2) append number if COMP does not have one

exec > /tmp/RL_check.zlog 2>&1

emulate -LR zsh
setopt xtrace
setopt extended_glob
setopt ksh_glob
setopt null_glob 

local PS4=$'+%1N:[%i]:%_> '


if [[ -e $1 ]]; then
	local PARENT=$(pwd)
	cd $1

#====================================================================================================
# functions {{{
#====================================================================================================

	# parameter character sort function for wrong swap filename
	function charsort(){ print $(print ${(L)1} | grep -o . | sort | tr -d '\n') }

	function report_append_convert(){ REPORT_CONVERT="${REPORT_CONVERT}${img}\n" }
	function report_append_rename(){ REPORT_RENAME="${REPORT_RENAME}${img}\n" }
	function report_append_manual(){ REPORT_MANUAL="${REPORT_MANUAL}${img}\n" }

	function rename_img(){ mv "${img}" "${img_product}_${cor_shot_name}.tif" }

	function rename_comp(){ 
		if [[ ${cor_shot_name} == "" ]]; then
			mv "${img}" "${img_product}_${img_shot}_${img_comp}.tif" 
		else
			mv "${img}" "${img_product}_${cor_shot_name}_${img_comp}.tif"
		fi
	}

#====================================================================================================
# }}}
#====================================================================================================

#====================================================================================================
# Variables {{{
#====================================================================================================
	rename -d ' ' *(.) # remove white space in filenames
	local currentRL_image=($(print -l *.(tif|tiff|TIF|TIFF))) # files in current session
	local currentRL_product=($(print -l $currentRL_image | cut -d_ -f1 | uniq)) # products in current session

	mkdir rename
	local RL_RENAME_DIR=rename/

	print "RL_check Report\n\nsession: $1\n\nno. of products: ${#currentRL_product}\nno. of images: ${#currentRL_image}\n\n" > rename/report
	local RL_report=rename/report

	local REPORT_CONVERT="images converted:\n\n"
	local REPORT_RENAME="images renamed:\n\n"
	local REPORT_MANUAL="manual rename required: ${img}\n\n"

#====================================================================================================
#}}}
#====================================================================================================

#====================================================================================================
# convert {{{
#====================================================================================================

	for img in $currentRL_image; do

		# reset array of correct file names
		typeset -a RL_shotname=(
				    BagAngle BagFront BagBack BagDetail1 BagDetail2 BagInterior BagReversible BagSide BagFrontOpen
				    ShoeAngle ShoeBack ShoeOverhead ShoeProfile ShoeDetail1 ShoeDetail2 ShoeBox ShoeSole
				    TABLETOP TT-DETAIL1 TT-DETAIL2 TT-DETAIL3
				    LAYDOWN LAYDOWNBACK SL-DETAIL1 SL-DETAIL2 SL-DETAIL3 FABRICDETAIL
				    BUST BUSTBACK
				   )

		# reset $cor_shot_name
		local cor_shot_name=""

		if [[ ${img} == *.(tiff|TIF|TIFF) ]]; then
			mv "${img}" "${img%.*}.tif"
			report_append_rename
			local img="${img%.*}.tif"
		fi

		# check and modify image spec (imagemagick as dependency)
		local img_spec=($(identify -format '%r %h %x %e %z' "${img}[0]"))
		cor_img_spec=0
		[[ ${img_spec[2]} == sRGB ]] && cor_img_spec=$(( $cor_img_spec + 1 ))
		[[ ${img_spec[3]} == 4000 ]] && cor_img_spec=$(( $cor_img_spec + 1 ))
		[[ ${img_spec[4]} == 300 ]] && cor_img_spec=$(( $cor_img_spec + 1 ))
		[[ ${img_spec[5]} == tif ]] && cor_img_spec=$(( $cor_img_spec + 1 ))
		[[ ${img_spec[6]} == 8 ]] && cor_img_spec=$(( $cor_img_spec + 1 ))

		if [[ ${cor_img_spec} == 5 ]]; then
			:
		elif [[ ${cor_img_spec} == 4 ]]; then
			if [[ ${img_spec[2]} != sRGB ]]; then
				convert -colorspace sRGB "${img}[0]" "${img}"
				report_append_convert
			elif [[ ${img_spec[3]} != 4000 ]]; then
				convert -resize x4000 "${img}[0]" "${img}"
				report_append_convert
			elif [[ ${img_spec[4]} != 300 ]]; then
				convert -resample 300 "${img}[0]" "${img}"
				report_append_convert
			elif [[ ${img_spec[5]} != tif ]]; then
				convert "${img}" "${img%.*}.tif"
				rm "${img}"
				local img="${img%.*}.tif"
				report_append_convert
			elif [[ ${img_spec[6]} != 8 ]]; then
				convert -depth "${img}[0]" "${img}"
				report_append_convert
			fi
		else
			convert -colorspace sRGB -resize x4000 -resample 300 -depth 8 "${img}" "${img%.*}.tif"
			rm "${img%.*}.(!(tif))" # remove $img that is not tif extension (ksh_glob required)
			local img="${img%.*}.tif"
			report_append_convert
		fi

#====================================================================================================
# }}}
#====================================================================================================

#====================================================================================================
# rename {{{
#====================================================================================================

		# check and rename image filename
		local img_product=$(print $img | cut -d_ -f1)
		local img_shot=$(print ${img:s/.tif//} | cut -d_ -f2)
		local img_comp=$(print ${img:s/.tif//} | cut -d_ -f3)

		# modify RL_shotname array to speedup loops
		if [[ ${(L)img_shot:0:3} == 'bag' ]]; then
			typeset -a RL_shotname=($(print -l $RL_shotname | grep -i bag))
		elif [[ ${(L)img_shot:0:4} == 'shoe' ]]; then
			typeset -a RL_shotname=($(print -l $RL_shotname | grep -i shoe))
		elif [[ ${(L)img_shot:0:5} == 'table' || ${(L)img_shot:0:2} == 'tt' ]]; then
			print -l $RL_shotname | grep '^T'
			typeset -a RL_shotname=($(print -l $RL_shotname))
		fi

		# rename comp
		if [[ ${img_comp} == "" ]]; then
			:
		elif [[ ${img_comp} == COMP[1-9] || ${img_comp} == 'INSERT' ]]; then #COMP or INSERT
			:
		elif [[ ${(U)img_comp} == COMP[1-9] || ${(U)img_comp} == 'INSERT' ]]; then #comp or insert
			local img_comp=${(U)img_comp}
			rename_comp
			report_append_rename
		elif [[ ${img_comp} == *[1-9] ]]; then #wrong spelling but end with digit
			local img_comp="COMP${img_comp[-1]}"
			rename_comp
			report_append_rename
		elif [[ $(charsort ${(U)img_comp}) == 'EINRST' ]]; then
			local img_comp="INSERT"
			rename_comp
			report_append_rename
		else 
			report_append_manual
			mv ${img} $RL_RENAME_DIR
			continue
		fi

		# rename shot name
		if [[ $(print "${RL_shotname}" | grep -w "${img_shot}") ]]; then #total correct shot name without comp
			continue 
		elif [[ $(print "${(L)RL_shotname}" | grep -w "${(L)img_shot}") ]]; then #correct name but different capital
			for cor_shot_name in $RL_shotname; do
				if [[ ${(L)cor_shot_name} == ${(L)img_shot} && ${img_comp} == "" ]]; then
					rename_img
					report_append_rename
					break
				elif [[ ${(L)cor_shot_name} == ${(L)img_shot} && ${img_comp} != "" ]]; then
					rename_comp
					report_append_rename
					break
				fi
			done
			continue
		else
			for cor_shot_name in $RL_shotname; do
				# rename image with swapped character
				if [[ $(charsort ${(L)cor_shot_name}) == $(charsort ${(L)img_shot}) && ${img_comp} == "" ]]; then
					rename_img
					report_append_rename
					continue 2
				elif [[ $(charsort ${(L)cor_shot_name}) == $(charsort ${(L)img_shot}) && ${img_comp} != "" ]]; then
					rename_comp
					report_append_rename
					continue 2
				fi

				for (( i=1; i<(( ${#cor_shot_name} + 2 )); i++ )); do 
					# rename image with missing 1 character
					# remove 1 character from cor_shot_name and compare with img_shot
					# problem: only the first alphabet will remove if there are two identical alphabets
					if [[ ${(L)cor_shot_name/${cor_shot_name[$i]}/} == ${(L)img_shot} && ${img_comp} == "" ]]; then
						rename_img
						report_append_rename
						continue 3
					elif [[ ${(L)cor_shot_name/${cor_shot_name[$i]}/} == ${(L)img_shot} && ${img_comp} != "" ]]; then
						rename_comp
						report_append_rename
						continue 3
					fi
					# rename image with 1 extra character
					# remove 1 character from img_shot and compare with cor_shot_name
					if [[ $(charsort ${(L)cor_shot_name}) == $(charsort ${img_shot/${img_shot[$i]}/}) && ${img_comp} == "" ]]; then
						rename_img
						report_append_rename
						continue 3
					elif [[ $(charsort ${(L)cor_shot_name}) == $(charsort "${img_shot/${img_shot[$i]}/}") && ${img_comp} != "" ]]; then
						rename_comp
						report_append_rename
						continue 3
					fi
				done
			done
			report_append_manual
			mv ${img} $RL_RENAME_DIR
		fi
	done
	
#====================================================================================================
# }}}
#====================================================================================================

	print "${REPORT_CONVERT}\n${REPORT_RENAME}\n${REPORT_MANUAL}" >> ${RL_report}
	open $RL_report
	cd $PARENT
else
	print " Missing: Ralph Lauren session folder"
	exit 2
fi

# vim: set foldmethod=marker foldlevel=0:
