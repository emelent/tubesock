$(function() {
	const interval = 2000
	const $videoList = $('#list-videos')
	const $input = $('#input-video-url')
	const $start = $('#start')
	const $duration = $('#duration')
	const $hd = $('#hd')
	const $audio = $('#audio')

	const queue = {}

	function onGoClick(){
		const url = $input.val()
		if (url === '') return

		const start = $start.val().trim()
		const duration = $duration.val().trim()
		const hd = $hd.is(":checked")
		const audio = $audio.is(":checked")

		$input.val('')
		$.ajax({
			type: 'POST',
			url: '/fetch',
			data: `url=${encodeURIComponent(url)}&start=${encodeURIComponent(start)}&duration=${encodeURIComponent(duration)}&hd=${encodeURIComponent(hd)}&audio=${encodeURIComponent(audio)}`,
			dataType: 'json',
			success({id}){
				// start polling
				console.log('let the polling begin')
				addQueueItem(id)
				poll(id)
			},
			fail(error){
				console.error('Failed =>', error)
			},
		})  
	}

	function addQueueItem(id){
		queue[id] = {busy: true}
		const $el = $(
			`<li id="item-${id}" class="list-group-item link">BUSY...</li>`
		)
		$videoList.append($el)
	}

	function addDownloadLink(id, title, url){
		$(`#item-${id}`)
			.html(`<span>${title}</span><a class="btn btn-primary download-btn" href="${url}">Download</a>`)
		$('download-btn').click(downloadBtn)
	}

	function downloadBtn(e){
		e.preventDefault()
		$el = $(this)
		window.location.href=$el.href
	}
	function poll(id){
		if(!queue[id].busy) return
		setTimeout(() => {
			$.ajax({
				type: 'GET',
				url: '/poll/' + id,
				dataType: 'json',
				success({result, error}){
					if (error){
						console.error('failed => ', error)
						queue[id].busy = false
						return
					}
					
					if(!result){
						console.log('polling again')
						poll(id)
						return
					}
					queue[id].busy = false
					if (result === 'FAIL') {
						alert("Download failed.")
						console.log('Oh, something went terribly wrong.')
						return
					}
					console.log('Download at =>', result.url)
					addDownloadLink(id, result.title, result.url)
				},
				fail(error){
					console.error('Failed =>', error)
				},
			}) 
		}, interval)
	}

	$('#btn-fetch').click(onGoClick)
})
