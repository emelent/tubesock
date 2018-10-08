$(function() {
	const interval = 2000
	let busy = false
	const $videoList = $('#list-videos')

	function onGoClick(){
		const url = $('#input-video-url').val()
		if (url === '' || busy) return

		console.log('fetching =>', url)
		
		$.ajax({
			type: 'POST',
			url: '/fetch',
			data: 'url='+encodeURIComponent(url),
			dataType: 'json',
			success({id}){
				// start polling
				console.log('let the polling begin')
				busy = true
				poll(id);
			},
			fail(error){
				console.error('Failed =>', error)
			},
		})  
	}

	function addDownloadLink(title, url){
		const $el = $(
			`<li class="list-group-item link">${title} <a class="btn btn-primary download-btn" href="${url}">Download</a></li>`
		)
		$videoList.append($el)
	}

	function poll(id){
		if(!busy) return
		setTimeout(() => {
			$.ajax({
				type: 'GET',
				url: '/poll/' + id,
				dataType: 'json',
				success({result, error}){
					if (error){
						console.error('failed => ', error)
						busy = false
						return
					}
					
					if(!result){
						console.log('polling again')
						poll(id)
						return
					}
					busy =false
					if (result === 'FAIL') {
						console.log('Oh, something went terribly wrong.')
						return
					}
					const downloadUrl = location.href + encodeURIComponent(result.url)
					console.log('Download at =>', downloadUrl)
					addDownloadLink(result.title, downloadUrl)
				},
				fail(error){
					console.error('Failed =>', error)
				},
			}) 
		}, interval)
	}

	$('#btn-fetch').click(onGoClick)
})
